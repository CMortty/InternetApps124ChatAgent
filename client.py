from model import Model
import view
from controller import Controller

print "We are on the client"

model = Model()
c = Controller(model)

view.getName()
model.clientInstantiate()
c.initiate()
c.clientLoop()