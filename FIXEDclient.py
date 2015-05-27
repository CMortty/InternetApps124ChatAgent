from network import Handler, poll
import sys
from threading import Thread
from time import sleep
import webbrowser

print "We are on the client"
myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        print "Goodbye!"
    
    def on_msg(self, msg):
        print msg
        
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
    elif mytxt ==":q":
        client.do_close()
    else:
        client.do_send({'speak': myname, 'txt': mytxt})
