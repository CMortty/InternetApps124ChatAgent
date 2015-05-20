from network import Listener, Handler
import view
import sys

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        view.printMsg(msg)
        
class MyHandler(Handler):
    
    handlers = {}  # map OLDclient handler to user name 
    prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."
    
    def on_open(self):
        pass
        
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        if 'join' in msg:
            self.handlers[msg['join']] = self
            self.do_send(self.prompt)
        else:
            view.printMsg(msg['speak'] + ": " + msg['txt'])
            mytxt = sys.stdin.readline().rstrip()
            self.do_send("Agent: " + mytxt)

class Model():
    
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        
    def clientInstantiate(self):
        self.client = Client(self.host, self.port)
    
    def serverInstantiate(self):
        self.server = Listener(self.port, MyHandler)
    