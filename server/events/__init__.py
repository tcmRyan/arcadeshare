from server.events.device import update_device, update_feed, update_game
from server.signals import *

device_updated.connect(update_device)
feed_updated.connect(update_feed)
game_updated.connect(update_game)
