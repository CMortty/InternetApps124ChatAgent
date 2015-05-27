from network import Listener, Handler
import collections
import view
import sys

class Client(Handler):
    
    def on_close(self):
        view.printMsg("Goodbye!")
        Model.running = False
    
    def on_msg(self, msg):
        view.printMsg(msg)
        
class MyHandler(Handler):
    
    
    handlers = {}  # map OLDclient handler to user name 
    waiting = collections.deque()
    prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."

    def on_open(self):
        pass
        
    def on_close(self):
        #Check to make sure someone is in the queue
        try:
            user = self.waiting.popleft()
            user.do_send(self.prompt)
            user.connected = False            
        except IndexError:
            pass
     
    def on_msg(self, msg):
        if 'join' in msg:
            self.handlers[msg['join']] = self
            if len(self.handlers) > 1:
                self.do_send("The agent is currently busy. Please wait...")
                self.waiting.append(self)
            else:
                self.do_send(self.prompt)
                self.connected=False
        else:
            if self in self.waiting:
                self.do_send("The agent is currently busy. Please wait...")
            else:
                if self.connected==True:
                    print(self.connected)
                    view.printMsg(msg['speak'] + ": " + msg['txt'])
                    mytxt = sys.stdin.readline().rstrip()
                    self.do_send("Agent: " + mytxt)
                    
                elif msg['txt']=='1' and self.connected==False:
                    self.do_send("One moment while we connect you to an agent to assist you with your order!")
                    self.connected=True
                    
                elif msg['txt']=='2' and self.connected==False:
                    self.do_send("One moment while we connect you to an agent who will take your feedback!")
                    self.connected=True
                    
                elif msg['txt']=='3' and self.connected==False:
                    self.do_send("One moment while we connect you to an agent that can answer your questions!")
                    self.connected=True
  
                else:
                    self.do_send("Please provide a valid input.")
                    self.do_send(self.prompt)

class Model():
    
    running = True
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        
    def clientInstantiate(self):
        self.client = Client(self.host, self.port)
    
    def serverInstantiate(self):
        self.server = Listener(self.port, MyHandler)
    
