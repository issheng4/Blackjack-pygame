import logging
from game.game_controller import GameController

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    game = GameController()
    game.run()