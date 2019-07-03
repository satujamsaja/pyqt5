"""
Run server in Thread
"""
from PyQt5.QtCore import QThread
import socketio
import eventlet
from chatNameSpace import ChatNameSpace
import yaml


class ChatThread(QThread):

    def __init__(self):
        super().__init__()

        # Socket IO init.
        self.sio = socketio.Server()
        self.sio.register_namespace(ChatNameSpace('/'))
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': 'index.html',
            '/static': '/static'
        })

        # Config.
        self.server_config = None

    def __del__(self):
        self.wait()

    def start_server(self):
        with open('server.yml', 'r') as config:
            server_config = yaml.load(config, Loader=yaml.SafeLoader)
            if server_config:
                self.server_config = server_config

        # Start server.
        if self.server_config is not None:
            host = self.server_config.get('host')
            port = int(self.server_config.get('port'))
            eventlet.wsgi.server(eventlet.listen((host, port)), self.app)

    def run(self):
        self.start_server()


