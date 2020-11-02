# Chat server and client with Python Socket IO
This app demonstrate how to create simple chat server and client using Python Socket Io and PyQT5

# Screenshot (Click for video)
[![Chat Demo App](https://github.com/satujamsaja/pyqt5/raw/master/chat/screenshot.jpg)](https://www.youtube.com/watch?v=2VmeBsuJ3Ck)
# Requirements
* Python 3+
* eventlet
* PyQt5
* PyYAML
* python-socketio
* requests

# How to install
* Setup your python virtual environtment
* Install above requirements using pip, from command prompt/terminal
  * $ pip install eventlet
  * $ pip install pyqt5
  * $ pip install pyyaml
  * $ pip install pythin-socketio
  * $ pip install requests

# How to run Server
* Go to server folder (server/)
* Run "python chat-server.py"
* Configure IP address and port and click "Start Server"

# Ho to run Client (client/)
* Go to client folder (client/)
* Run "python chat-client.py"
* From menu click "Chat" and click "Connect"
* Enter server IP Address and Port
* Click "Ok" to connect

# How to simulate or test the chat
* Run server and several clients
* Connects clients to server
* Configure nickname and channels for clients to connect
* Start type on text field and click "Send"

# Expected result
* Each connected client on same channel should communicate in the same channel
* No broadcast communication (client can send message to different channel)
* It should be realtime fast


