import json
import time

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import esp

esp.osdebug(None)

import gc
gc.collect()

ssid = 'Space_2G'
password = '13579236rQ'

station = network.WLAN(network.STA_IF)

station.active(True)
time.sleep(3)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)

led_state = "OFF"
def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>ESP MicroPython Web Server</h2>
    <p>LED state: <strong>""" + led_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?led_2_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a id="led_off" onclick="mode()" ><button class="button button1">LED OFF</button></a>
        <script>
            function mode(){
                alert($('#led_off').text());
                params = {'name': 'loh'}
                $.ajax({
                    url: '/',
                    method: 'post',
                    data: params,
                    success: function (data) {
                        alert(data.answer);
                    }
                });
            }
        </script>
    </p>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    </p>
</body>

</html>"""
    return html

def json_data():
    data = {'answer': 'idi nahui'}
    return json.dumps(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Request Content = %s' % request)
        response = ''
        if 'POST' in request and 'loh' in request:
            response = json_data()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Connection: close\n\n')
        if 'GET' in request:
            if 'led_2_on' in request:
                print('LED ON -> GPIO2')
                led_state = "ON"
                led.on()
            if 'led_2_off' in request:
                print('LED OFF -> GPIO2')
                led_state = "OFF"
                led.off()
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')