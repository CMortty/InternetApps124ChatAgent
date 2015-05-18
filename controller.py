from network import poll
from time import sleep
import webbrowser
from threading import Thread
import sys
import view

class Controller():
    
    def __init__(self, model):
        self.model = model
        
    def periodic_poll(self):
        while 1:
            poll()
            sleep(0.05)  # seconds
            
    def initiate(self):
        self.model.client.do_send({'join': view.myname})
        
    def clientLoop(self):
        thread = Thread(target=self.periodic_poll)
        thread.daemon = True  # die when the main thread dies 
        thread.start()

        while 1:
            mytxt = sys.stdin.readline().rstrip()
            if mytxt == ":e":
                webbrowser.open_new("http://upload.wikimedia.org/wikipedia/en/2/20/Captain_Picard_Chair.jpg")
            else:
                self.model.client.do_send({'speak': view.myname, 'txt': mytxt})
    
    def serverLoop(self):
        while 1:
            poll(timeout=0.05) # in seconds