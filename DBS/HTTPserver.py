"""
! Has Bugs
! If your goal is “fake the sensor”, you should publish MQTT instead of doing HTTP POST.

!If you want to simulate the sensor correctly:
!Use MQTT publish (like your mqtt_publish_wl.py) instead of HTTP.


In the `HTTPserver.py` Java server, `/api/systemdata` is a GET endpoint used by the endpoint
used by the dashboard to *read* current system data.

This line (87):
response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
is wrong, and will respond with "404", or "405", meaning "Method Not Allowed".

"""




import requests    # Make HTTP requests (client)
import json        # parse/encode JSON
import random      # Generate random values
import time        # Sleep between sends

# Build-in simple HTTP server
from http.server import BaseHTTPRequestHandler, HTTPServer

import threading  # Run the server in a background thread (so main loop keeps sending)

#######################################
# TINY SERVER (PORT 8051) - RECEIVER  #
#######################################

# Defines a request handler class. 
# Each incoming HTTP request is handled by methods do_GET, do_POST, etc...

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # do_POST method is called when someone sends an HTTP POST to server (localhost:8051)
    def do_POST(self):
        # Reads content lenght
        content_length = int(self.headers['Content-Length'])
        # Reads raw data
        post_data = self.rfile.read(content_length)
        #? Parses the body as JSON into a Python dict.
        # If the client sends invalid JSON → this throws an exception and the server will error.
        data = json.loads(post_data)
        # Prints whatever was received.
        print("Received data: ", data)

        self.send_response(200)         # Sends HTTP status 200
        self.end_headers()
        self.wfile.write(b'Success')    # and the body "Success"


# ----------- Start server -----------
# Starts server in another thread
httpd = HTTPServer(('localhost', 8051), SimpleHTTPRequestHandler)
# Creates the server socket: host=localhost, port=8051, using handler
thread = threading.Thread(target=httpd.serve_forever)

# Runs the server loop forever in a background thread.
# Without this, while True loop would prevent the server from running.
thread.start()


#######################################
#                CLIENT               #
#######################################

# Where we want to send data to
#! I modified here the original file
url = 'http://127.0.0.1:8050/api/postdata'

while True:
    # Fake values for wl and valveValue
    wl = random.randint(1, 100)
    valveValue = random.randint(1, 100)

    # Set fake status to "SAMPLE_STATUS"
    status = "SAMPLE_STATUS"

    #! I modified here the original file
    # Builds JSON payload
    payload = {
    "isManual": True,
    "valveValue": valveValue
}

    # Debug output
    print("Sending payload: ", payload)

    # Sends HTTP POST with JSON body.
    #! I modified here the original file
    response = requests.post(url, json=payload)

    # Prints backend response.
    print(response.text)

    # Wait 1 second
    time.sleep(1)