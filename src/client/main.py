import pygame
from level import Level

LEVEL_MAP = [[0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0]]

PLAYER_MAP = [[1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],]

BOMB_MAP = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],]

CELL_SIZE = 50


def main():
    height = len(LEVEL_MAP)
    width = len(LEVEL_MAP[0])
    display_height = height * CELL_SIZE
    display_width = width * CELL_SIZE


    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("DisSysBomberman")
    level = Level(LEVEL_MAP, PLAYER_MAP, BOMB_MAP, CELL_SIZE)
    game_loop = GameLoop(level, CELL_SIZE, display, 1)


    pygame.init()
    game_loop.start()

    


class GameLoop:
    def __init__(self, level, cell_size, display, player_id):
        self._level = level
        self._clock = pygame.time.Clock()
        self._cell_size = cell_size
        self._display = display
        self._player_id = player_id

    def start(self):
        while True:
            if self._handle_events() == False:
                break

            self._render()

            self._clock.tick(60)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.level.move_player(self._player_id, -1, 0, CELL_SIZE)
                if event.key == pygame.K_RIGHT:
                    self.level.move_player(self._player_id, 1, 0, CELL_SIZE)
                if event.key == pygame.K_UP:
                    self.level.move_player(self._player_id, 0, -1, CELL_SIZE)
                if event.key == pygame.K_DOWN:
                    self.level.move_player(self._player_id, 0, 1, CELL_SIZE)
            elif event.type == pygame.QUIT:
                return False

    def _render(self):
        self._level.update(2)
        self._level.render(self._display)
        
        pygame.display.update()

if __name__ == "__main__":
    main()