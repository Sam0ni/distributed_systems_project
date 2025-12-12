import time
from queue import Queue
from objects.player import PlayerObject
from leader import Leader
from follower import Follower
from services.peer_comms import PeerComms

class ServerLoop:
    def __init__(self, server_id, peers_config, level_map, player_map, bomb_map, explosion_map, tick_rate=60):
        self.server_id = server_id
        self.peers_config = peers_config
        self.tick_rate = tick_rate
        self.tick_interval = 1.0 / tick_rate

        self.heartbeat_interval = 30
        self.last_heartbeat_sent = 0

        self.last_heartbeat_tick = 0
        self.heartbeat_timeout = 120
        
        self.global_tick = 0
        self.level_map = level_map
        self.player_map = player_map
        self.bomb_map = bomb_map
        self.explosion_map = explosion_map
        self.players = {}
        self.bombs = {}
        self.explosions = {}
        
        self.global_bomb_id = 1
        self.global_explosion_id = 1
        self.new_player_id = 1

        self.role_obj = Follower(self)
        self.leader_addr = None
        self.leader_id = None
        self.has_leader = False
        self.peer_queue = Queue()
        self.peer_comms = PeerComms(self.server_id, self.peers_config, self.peers_config[server_id-1][2], self.peer_queue)

        self.election_in_progress = False
        self.waiting_for_leader = False
        self.election_start_time = None
        self.election_timeout = 0.2

        self.initialize_players()

    def initialize_players(self):
        height = len(self.level_map)
        width = len(self.level_map[0])
        for y in range(height):
            for x in range(width):
                cell = self.player_map[y][x]
                if cell != 0:
                    self.players[cell] = PlayerObject(cell, x, y)

    def start(self):
        """Decides role based on ID and availability of peers"""
        print(f"Server {self.server_id} starting...", flush=True)
        
        while True:
            if not self.has_leader:
                self.run_bully()
            self.waiting_for_leader = False
            result = self.role_obj.run()

            match result:
                case "NEED_ELECTION":
                    self.has_leader = False
                    continue
                case "DEMOTION":
                    self.role_obj = Follower(self)
                    continue
                case "LEADER_SWITCH":
                    continue
            

    def run_bully(self):
        print("Starting election", flush=True)

        self.start_election()
        self.election_in_progress = True

        while True:
            while not self.peer_queue.empty():
                msg = self.peer_queue.get()
                if msg["type"] == "leader_announce":
                    self.has_leader = True
                    self.role = Follower(self)
                    self.leader_id = msg["from"]
                    self.leader_addr = self.peers_config[msg["from"] - 1]
                    return
                elif msg["type"] == "bully_ok":
                    self.waiting_for_leader = True
                    pass
                elif msg["type"] == "bully":
                    self.handle_bully(msg["from"])
                
            if not self.waiting_for_leader and self.election_timeout_expired():
                self.become_leader()
                self.has_leader = True
                return
            
            time.sleep(0.001)

    def start_election(self):
        msg = {
            "type": "bully",
            "from": self.server_id
        }

        self.peer_comms.broadcast(msg)
        self.election_start_time = time.perf_counter()

    def handle_bully(self, from_id):
        msg = {
            "type": "bully_ok",
            "from": self.server_id
        }
        self.peer_comms.send_to_peer(from_id, msg)

    def become_leader(self):
        self.role_obj = Leader(self)
        msg = {
            "type": "leader_announce",
            "from": self.server_id
        }
        self.peer_comms.broadcast(msg)

    def election_timeout_expired(self):
        if self.election_start_time is None:
            return False
        now = time.perf_counter()
        return (now - self.election_start_time) >= self.election_timeout