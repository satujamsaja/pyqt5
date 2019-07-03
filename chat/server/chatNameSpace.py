import socketio


class ChatNameSpace(socketio.Namespace):

    def on_join(self, sid, message):
        self.enter_room(sid, message['room'])
        self.emit('server_message', {'data': 'Entered room: ' + message['room']}, room=sid)

    def on_leave(self, sid, message):
        self.leave_room(sid, message['room'])
        self.emit('server_message', {'data': 'Left room: ' + message['room']}, room=sid)

    def on_close_room(self, sid, message):
        self.emit('server_message',  {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
        self.close_room(message['room'])

    def on_room_event(self, sid, message):
        self.emit('room', {'data': message['data']}, room=message['room'], skip_sid=sid)

    def on_disconnect_request(self, sid):
        self.emit('server_message', {'data': 'Request disconnect: ' + sid})
        self.disconnect(sid)

    def on_connect(self, sid, environ):
        self.emit('server_message', {'data': 'Connected: ' + sid, 'count': 0}, room=sid)

    def on_disconnect(self, sid):
        self.emit('server_message', {'data': 'Disconnected: ' + sid}, room=sid)
