from network import Listener, Handler, poll
import collections

 
handlers = {}  # map client handler to user name
waiting = collections.deque()
prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."

print "We are on the server" 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        for name, h in handlers.items():
            if h == self:
                del handlers[name]
        user = waiting.popleft()
        handlers[user[0]] = user[1]
        user[1].do_send(prompt)        
     
    def on_msg(self, msg):
        if 'join' in msg:
            if len(handlers) >= 2:
                waiting.append((msg['join'], self))
                self.do_send("Please wait for next available agent")
            else:
                handlers[msg['join']] = self
                self.do_send(prompt)
        else:
            if (msg['speak'], self) in waiting:
                self.do_send("Please wait for next available agent") 
            else:
                for name in handlers.keys():
                    if name != msg['speak']:
                        handlers[name].do_send(msg['speak'] + ": " + msg['txt'])

 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


