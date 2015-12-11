import view
from controller import Controller

print("We are on the client")

c = Controller()

view.getName()
c.clientInstantiate()
c.connectToServer()
c.clientLoop()
