from server.signals import *
from .game_pub import *

game_created.connect(game_created_pub)
game_updated.connect(game_updated_pub)
