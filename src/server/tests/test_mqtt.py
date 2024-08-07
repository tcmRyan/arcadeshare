import paho.mqtt.client as mqtt


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connecto with result code " + str(rc))
    client.subscribe("testtopic/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.username_pw_set("ryan2", "test2")

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.publish("emqtt", payload="Hello World", qos=0)
# Infinite loop - check SCRUM-10
# client.loop_forever()
