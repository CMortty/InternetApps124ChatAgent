from network import poll, Handler, Listener
from time import sleep
import webbrowser
from threading import Thread
import sys
import view
from model import Model

class Controller():
        
    def periodic_poll(self):
        while 1:
            poll()
            sleep(0.05)  # seconds
            
    def connectToServer(self):
        self.client.do_send({'join': view.myname})
        
    def clientLoop(self):
        thread = Thread(target=self.periodic_poll)
        thread.daemon = True  # die when the main thread dies 
        thread.start()

        while Model.running:
            mytxt = sys.stdin.readline().rstrip()
            if mytxt == ":e":
                webbrowser.open_new("http://upload.wikimedia.org/wikipedia/en/2/20/Captain_Picard_Chair.jpg")
            elif mytxt ==":q":
                self.client.do_close()
            else:
                self.client.do_send({'speak': view.myname, 'txt': mytxt})
    
    def serverLoop(self):
        while 1:
            poll(timeout=0.05) # in seconds
            
    def clientInstantiate(self):
        self.client = Client(Model.host, Model.port)
    
    def serverInstantiate(self):
        self.server = Listener(Model.port, MyHandler)

class Client(Handler):
    
    def on_close(self):
        view.printMsg("Goodbye!")
        Model.running = False
    
    def on_msg(self, msg):
        view.printMsg(msg)
        
class MyHandler(Handler):

    def on_open(self):
        pass
        
    def on_close(self):
        for name, h in Model.handlers.items():
            if h == self:
                del Model.handlers[name]
                self.sendToAll("I disconnected.", name)
        try:
            user = Model.waiting.popleft()
            Model.handlers[user[0]] = user[1]
            user[1].do_send(Model.prompt)
            user[1].conn = False
        except IndexError:
            pass 
     
    def on_msg(self, msg):
        if 'join' in msg:
            if len(Model.handlers) == 0:
                Model.handlers[msg['join']] = self
                self.conn = True
            elif len(Model.handlers) >= 2:
                Model.waiting.append((msg['join'], self))
                self.do_send("Please wait for next available agent")
            else:
                Model.handlers[msg['join']] = self
                self.do_send(Model.prompt)
                self.conn = False
        else:
            if (msg['speak'], self) in Model.waiting:
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
                    self.do_send(Model.prompt)
                    
    def sendToAll(self, msg, myName):
        for name in Model.handlers.keys():
            if name != myName:
                Model.handlers[name].do_send(myName + ": " + msg)