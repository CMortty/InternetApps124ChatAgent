from network import Listener, Handler, poll
import collections
import sys
 
handlers = {}  # map OLDclient handler to user name
waiting = collections.deque()
prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."
print "We are on the server"
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
#         self.do_close()
#Check to make sure someone is in the queue
        user = waiting.popleft()
        user.do_send(prompt)
     
    def on_msg(self, msg):
        if 'join' in msg:
            handlers[msg['join']] = self
            if len(handlers) > 1:
                self.do_send("The agent is currently busy. Please wait...")
                waiting.append(self)
            else:
                self.do_send(prompt)
        else:
            if self in waiting:
                self.do_send("The agent is currently busy. Please wait...")
            else:
                print msg['speak'] + ": " + msg['txt']
                mytxt = sys.stdin.readline().rstrip()
                self.do_send("Agent: " + mytxt)
 
 
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


