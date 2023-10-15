import socketio, time


class sioclient():
    def __init__(self):
        print('Create python socket.io object')
        self.sio = socketio.Client(reconnection = True, reconnection_delay=0.1, request_timeout = 0.1)
        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("msg_gui", self.on_msg_gui)
        self.sio.on("msg_server", self.on_msg_gui)
        self.sio.on("askForUserId", self.on_msg_askforuserid)
        
        
    def on_connect(self):
        print('connection established')
        
    def on_msg_gui(self, data):
        print('gui message received with ', data)
        print(self.sio.eio.sid)
        print('request id is ' + data["receiverId"])
        print('request data is ' + data["data"])
        print("do something.... processing...")
        answer = {"receiverId" : data["receiverId"], 
            "data" : f'This is engine answer for single client.. {data["receiverId"]}'}
        self.send("reply_engine", answer)
      
    
    def on_msg_askforuserid(self):
        self.sio.emit('userIdReceived', self.sio.eio.sid);

    
    def on_disconnect(self):
        print('disconnected from server')
        
    def connect(self, address):
        self.address = address

        result = False
        try:
            self.sio.connect(address)
            result = True
        except Exception as e:
            print(e)
            result = False
        finally:
            return result

    def isconnected(self):
        return self.sio.connected

    def disconnect(self):
        try:
            self.sio.disconnect()
        except Exception as e:
            print(e)

    def send(self, name_event, data):
        try:
            self.sio.emit(name_event, data)
        except Exception as e:
            print(e)

    
s = sioclient()
print(s.connect('http://localhost:5000'))

count = 0
while True:
    print(f'main loop..{count}')
    s.send("msg_engine", {"data" : f'engine message... {count}'})
    time.sleep(1)
    count += 1
    