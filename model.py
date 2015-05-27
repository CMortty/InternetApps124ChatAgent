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
        for name, h in self.handlers.items():
            if h == self:
                del self.handlers[name]
        try:
            user = self.waiting.popleft()
            self.handlers[user[0]] = user[1]
            user[1].do_send(self.prompt)
            user[1].conn = False
        except IndexError:
            pass 
     
    def on_msg(self, msg):
        if 'join' in msg:
            if len(self.handlers) == 0:
                self.handlers[msg['join']] = self
                self.conn = True
            elif len(self.handlers) >= 2:
                self.waiting.append((msg['join'], self))
                self.do_send("Please wait for next available agent")
            else:
                self.handlers[msg['join']] = self
                self.do_send(self.prompt)
                self.conn = False
        else:
            if (msg['speak'], self) in self.waiting:
                self.do_send("Please wait for next available agent") 
            else:
                if self.conn==True:
                    self.sendToAll(msg['txt'], msg['speak'])
                    
                elif msg['txt']=='1' and self.conn==False:
                    self.do_send("You are now connected to an agent to assist you with your order!")
                    self.sendToAll("You are assisting me with an order!", msg['speak'])
                    self.conn=True
                    
                elif msg['txt']=='2' and self.conn==False:
                    self.do_send("You are now connected to an agent who will take your feedback!")
                    self.sendToAll("You are taking my feedback!", msg['speak'])
                    self.conn=True
                    
                elif msg['txt']=='3' and self.conn==False:
                    self.do_send("You are now connected to an agent that can answer your questions!")
                    self.sendToAll("You are answering my questions!", msg['speak'])
                    self.conn=True
  
                else:
                    self.do_send("Please provide a valid input.")
                    self.do_send(self.prompt)
                    
    def sendToAll(self, msg, myName):
        for name in self.handlers.keys():
            if name != myName:
                self.handlers[name].do_send(myName + ": " + msg)

class Model():
    
    running = True
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        
    def clientInstantiate(self):
        self.client = Client(self.host, self.port)
    
    def serverInstantiate(self):
        self.server = Listener(self.port, MyHandler)
    
