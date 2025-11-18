import pygame
from sprites.player import Player
from objects.playerObject import PlayerObject
from sprites.floor import Floor
from sprites.wall import Wall

class Level:
    def __init__(self, level_map, player_map, bomb_map, cell_size):
        self.cell_size = cell_size
        self.players = {}
        self.level_map = level_map
        self.player_map = player_map
        self.bomb_map = bomb_map
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()

        self.static_sprites = pygame.sprite.Group()

    def _initialize_sprites(self, level_map):
        height = len(level_map)
        width = len(level_map[0])

        for y in range(height):
            for x in range(width):
                cell = level_map[y][x]
                normalized_x = x*self.cell_size
                normalized_y = y*self.cell_size

                if cell == 0:
                    self.floors.add(Floor(normalized_x, normalized_y))
                elif cell == 1:
                    self.walls.add(Wall(normalized_x, normalized_y))

        self.static_sprites.add(self.walls, self.floors)

        for y in range(height):
            for x in range(width):
                cell = level_map[y][x]
                normalized_x = x*self.cell_size
                normalized_y = y*self.cell_size

                if cell == 0:
                    continue
                else:
                    self.players[cell] = PlayerObject(cell, x, y, Player(x, y))

    def update(self, dt):
        for player in self.players.values():
            player.update(dt)

    def render(self, screen):
        self.static_sprites.draw(screen)

        for player in self.players.values():
            player.render(screen)

    def move_player(self, id, x, y, amount):
        player_x = self.players[id].x
        player_y = self.players[id].y
        new_x = player_x + x
        new_y = player_y + y

        if (0 < new_x < len(self.level_map[0])) and (0 < new_y < len(self.level_map)):
            if self.level_map[new_y][new_x] != 0:
                return False
            elif self.player_map[new_y][new_x] != 0:
                return False
            else:
                self.player_map[player_x][player_y] = 0
                self.player_map[new_x][new_y] = id
                self.players[id].move(x, y, amount)
                return True

        else:
            return False