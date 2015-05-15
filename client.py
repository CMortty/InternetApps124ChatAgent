from network import Handler, poll
import sys
from threading import Thread
from time import sleep
import view
import webbrowser

myname = view.getName()

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        view.printMsg(msg)
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while 1:
    mytxt = sys.stdin.readline().rstrip()
    if mytxt == ":e":
        webbrowser.open_new("http://upload.wikimedia.org/wikipedia/en/2/20/Captain_Picard_Chair.jpg")
    else:
        client.do_send({'speak': myname, 'txt': mytxt})
