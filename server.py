from network import Listener, Handler, poll

 
handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        if 'join' in msg:
            handlers[msg['join']] = self
        else:
            for name in handlers.keys():
                if name != msg['speak']:
                    handlers[name].do_send(msg['speak'] + ": " + msg['txt'])
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


