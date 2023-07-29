import pusherclient
import json

pusher = pusherclient.Pusher('c0eef4118084f8164bec65e6253bf195', {
    'encrypted': True,
    'ws_port': 443,
    'wss_port': 443,
    'host': 'notifier.bitskins.com'
})

@pusher.connection.bind('connected')
def connected():
    # connected to realtime updates
    print(" -- connected to websocket")

@pusher.connection.bind('disconnected')
def disconnected():
    # not connected to realtime updates
    print(" -- disconnected from websocket")

events_channel = pusher.subscribe("inventory_changes")  # use the relevant channel, see docs below

@events_channel.bind("listed")
def event_handler(data):
    # use the relevant event type, see docs below
    # print out any data received for the given event type
    print(" -- got data: " + json.dumps(data))

# Implement a callback function for the bind() method
def dummy_callback(data):
    print("Callback function executed:", data)

# Bind the "listed" event to the callback function
events_channel.bind("listed", dummy_callback)

# Start the pusher connection
pusher.connect()

# Keep the program running to receive events
while True:
    pass