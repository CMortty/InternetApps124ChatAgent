from model import Model
from controller import Controller

print "We are on the server"

model = Model()
c = Controller(model)

model.serverInstantiate()
c.serverLoop()