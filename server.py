from network import Listener, Handler, poll
import sys
 
handlers = {}  # map client handler to user name
prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."
print "We are on the server"
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        if 'join' in msg:
            handlers[msg['join']] = self
            self.do_send(prompt)
        else:
            print msg['speak'] + ": " + msg['txt']
            mytxt = sys.stdin.readline().rstrip()
            self.do_send("Agent: " + mytxt)
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


