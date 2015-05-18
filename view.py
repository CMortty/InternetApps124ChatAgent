class View():
    
    
    ####CHECK THIS####
    def __init__(self, model):
        self.model = model

myname = ""
def getName():
    global myname
    myname = raw_input('What is your name? ')
    return myname
    
def printMsg(msg):
    print msg