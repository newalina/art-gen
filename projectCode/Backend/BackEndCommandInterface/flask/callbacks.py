import json
import base64
# me - this DAT
# dat - the WebSocket DAT

def onConnect(dat):
	print("Connected to WebSocket.")
    # You might want to send a message right after connecting
	dat.sendText("Hello from TouchDesigner!")
​
# me - this DAT
# dat - the WebSocket DAT
def onDisconnect(dat):
	return
​
# me - this DAT
# dat - the DAT that received a message
# rowIndex - the row number the message was placed into
# message - a unicode representation of the text
# 
# Only text frame messages will be handled in this function.
def onReceiveText(dat, rowIndex, message):
	print("Received message:", message)
    # Assuming the incoming message is JSON with a structure like {"slider": value}
	try:
		data = json.loads(message)
		if 'slider' in data:
			slider_value = data['slider']
            # Process the slider value as needed
			print("Slider value received:", slider_value)
            # Optionally, send a response or acknowledgment back
			dat.sendText(f"Slider value {slider_value} received.")
	except Exception as e:
		print("Error processing message:", e)
    
# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only binary frame messages will be handled in this function.
​
def onReceiveBinary(dat, contents):
	return
​
# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only ping messages will be handled in this function.
​
def onReceivePing(dat, contents):
	dat.sendPong(contents) # send a reply with same message
	return
​
# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message content
# 
# Only pong messages will be handled in this function.
def onReceivePong(dat, contents):
	return

# me - this DAT
# dat - the DAT that received a message
# message - a unicode representation of the message
#
# Use this method to monitor the websocket status messages
​
def onMonitorMessage(dat, message):
	return

def send_data(dat, data):
    """Send data through the WebSocket.
    
    Args:
        dat: The WebSocket DAT.
        data: The data to send as a string.
    """
	# encode the data as a byte array using base64
    encoded_data = base64.b64encode(data.encode('utf-8'))
    # send the data to the front end
    dat.sendBinary(encoded_data)