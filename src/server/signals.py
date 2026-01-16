from blinker import Namespace

events = Namespace()
tenant_provisioned = events.signal("tenant-provisioned")
game_created = events.signal("game-created")
game_updated = events.signal("game-updated")
device_created = events.signal("device-created")
device_updated = events.signal("device-updated")
feed_created = events.signal("feed-created")
feed_updated = events.signal("feed-updated")
