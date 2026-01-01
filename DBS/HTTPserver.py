"""
The 4 biggest issues (why it might not run)

Duplicate dcc.Interval id "interval-component" (must be unique).

send_valveValue callback:

output property wrong (Button has no value)

no return statement

Some callbacks return nothing in some cases (Dash expects a return for all paths).

No error handling around requests.get() / requests.post() → if Java server not running, it crashes.
"""


from flask import Flask, request #TODO: Use or Remove the request import, because right now we dont use it

import dash                                         # This is the Dashboard framework
from dash import html, dcc                          # These are dash components (HTML tags, graphs, sliders...)
from dash.dependencies import Input, Output, State  # States for reactive functions

import plotly.graph_objs as go  # Makes graphs

from collections import deque   # Used to keep a sliding window
import datetime                 # Timestamps
import requests                 # to do HTTP calls to Java backend
import json                     # To convert from Python to Json

# Creates a queue that stores 60 items (data)
data_queue = deque(maxlen=60)

# --------- Flask Initialization -----------
# Creates flask object
server = Flask(__name__)
# Creates Dash app attached to flask server
app = dash.Dash(__name__, server=server, title="Dashboard")

# --------- UI Layout -----------
# TODO: change labels 
app.layout = html.Div([                #Root element is a <div>
    dcc.Interval(                      # Creates a timer that ticks every 1000 ms (1 s)
        id="interval-component",
        interval=1*1000,  # in milliseconds
        n_intervals=0     # every tick increments n_intervals
        #! Callbacks using Input("interval-component","n_intervals") will run every second.
    ),
    html.H1("Dashboard", style={"text-align": "center", "font-size": "48px"}), # Title
    html.Div([
        #TODO: change id
        html.Div([
            dcc.Graph(id="water-level-graph"),                     # Graph 1, side by side
        ], style={"width": "50%", "display": "inline-block"}),
        html.Div([
            dcc.Graph(id="valve-level-graph"),
        ], style={"width": "50%", "display": "inline-block"})      # Graph 2
    ]),
    #! BUG: ID is same as previous Interval, they should be unique.
    #! You only need ONE Interval.
    dcc.Interval(
        id="interval-component",
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    # Status text
    # TODO: changed based on specs
    html.Div(id="status-display",style={"text-align": "center", "font-size": "24px"}),

    # -------- Controls Row -----------

    html.Div([
        html.H3("Set Valve Value"),  # Heading for the controls
        html.Div([
            dcc.Slider(              # A slider named valveValue
            id='valveValue',         # range 0-100, default 0
            min=0,                   # marks creates labels every 10%
            max=100,
            value=0,
            marks={i: '{}%'.format(i) for i in range(0, 101, 10)},
            )], style={"width": "33%", "display": "inline-block"}),

            # A button that starts with n_clicks = 0, and increments each click
            html.Button("Set Valve Value", id="send-valveValue", n_clicks=0, className="button-17", style={"margin-right": "1%"}),
            
            # Another button for auto mode
            html.Button("Set Auto-mode", id="send-autoMode", n_clicks=0, className="button-17 button-17-red")

            # Uses flexbox to align slider + buttons nicely in a row.
    ], style={"display": "flex", "justify-content": "center", "align-items": "center"}),
    html.Div(id="dummy-output", style={"display": "none"}),   # Dummy outputs (TODO: Understand)
    html.Div(id="dummy-output1", style={"display": "none"})
])

#######################################
# CALLBACK 1
#######################################

# TODO: Understand
# This callback runs every second.
# It “outputs” something to dummy-output1.children (hidden), 
# but the real goal is the side effect: fetch and store state.
@app.callback([Output("dummy-output1", "children"),
              Input("interval-component", "n_intervals")])
def get_post_data(n_intervals): 

    url = "http://localhost:8050/api/systemdata"  
    response = requests.get(url)      # Calls Java backend
    
    data = response.json()[0]         # [{"wl":..., "valveValue":..., "status":...}]
    
    global data_queue    # We will use the global variable data_queue

    # Stores data we received
    data["wl"] = float(data["wl"])
    data["valveValue"] = int(data["valveValue"])
    data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Add time stamps to data

    data_queue.append(data)   # Add data to queue (max 60)

    # Prints to console (to debug)
    print("Data:")
    print(data_queue)
    return [""]      # Returns an empty string as children for dummy output.


#######################################
# CALLBACK 2
#######################################

@app.callback([
        Output("dummy-output", "children"),
        Input("send-autoMode", "n_clicks")   # Runs whenever the Auto-mode button is clicked.
        ])
def send_manualMode(n_clicks):
    url = "http://localhost:8050/api/postdata"
    if n_clicks is None:
        return [""]
    else:
        # Sends a command to turn automatic mode on
        data = {
            "isManual": False
        }
        # POSTs JSON payload to backend.
        response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        
        # Prints server response and puts it in hidden output div.
        print(response.text)
        return [f"Sent request with response: {response.text}"]
    

#######################################
# CALLBACK 3
#! Has a BUG
#######################################

'''
Runs when “Set Valve Value” clicked.
Reads slider value as State("valveValue","value").

Bug: Output is "send-valveValue", "value".
send-valveValue is a Button.
Buttons dont really have a meaningful value property in Dash 
(you usually update children or update a separate Div).
This often causes a Dash error like "Property 'value' was used with component ID ... 
which does not support this property".


Sends {"valveValue": <slider>} to backend.

Another practical issue: if backend requires isManual: 
true to actually apply, youre not sending it.
Also: this callback does not return anything →
Dash will complain because every callback must return something for its Output.
'''

@app.callback(Output("send-valveValue", "value"),
              [Input("send-valveValue", "n_clicks")],
              [State("valveValue", "value")])
def send_valveValue(n_clicks, valveValue):
    url = "http://localhost:8050/api/postdata"
    if n_clicks > 0:
        data = {
            "valveValue": valveValue
        }
        response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        print(response.text)


#######################################
# CALLBACK 4
#######################################

# Updates graph
@app.callback(Output("water-level-graph", "figure"),
              [Input("interval-component", "n_intervals")])
def update_water_level_graph(n):
    global data_queue

    # Crea il grafico utilizzando tutti i dati nella coda
    fig = go.Figure(
        data=[
            go.Scatter(
                x=[data["timestamp"] for data in data_queue],
                y=[data["wl"] for data in data_queue],
                mode="lines+markers",
                line=dict(color="blue")
            )
        ],
        layout=go.Layout(
            title=dict(text="Livello dell'acqua", font=dict(size=24, family="Roboto"), x=0.5),
            xaxis=dict(title="Ora"),
            yaxis=dict(title="Livello dell'acqua")
        )
    )

    return fig


#######################################
# CALLBACK 5
#######################################

# Update second graph
@app.callback(Output("valve-level-graph", "figure"),
              [Input("interval-component", "n_intervals")])
def update_valve_level_graph(n):
    global data_queue

    # Crea il grafico utilizzando tutti i dati nella coda
    fig = go.Figure(
        data=[
            go.Scatter(
                x=[data["timestamp"] for data in data_queue],
                y=[data["valveValue"] for data in data_queue],
                mode="lines+markers",
                line=dict(color="red")
            )
        ],
        layout=go.Layout(
            title=dict(text="Livello della valvola", font=dict(size=24, family="Roboto"), x=0.5),
            xaxis=dict(title="Ora"),
            yaxis=dict(title="Livello della valvola")
        )
    )

    return fig


#######################################
# CALLBACK 6
#######################################

# Updates status display
#! Note: if queue empty, returns nothing → should return something (like empty string) to be safe.
@app.callback(Output("status-display", "children"),
              [Input("interval-component", "n_intervals")])
def update_status_display(n):
    global data_queue
    if data_queue:
        return f'Stato del sistema: {data_queue[-1]["status"]}'
    

# -------- MAIN ----------
# Start server
if __name__ == "__main__":
    app.run_server(debug=True, port=8057)