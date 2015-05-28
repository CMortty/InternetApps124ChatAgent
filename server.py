from controller import Controller

print "We are on the server"

c = Controller()

c.serverInstantiate()
c.serverLoop()