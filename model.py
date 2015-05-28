import collections


class Model():
    prompt = "Thank you for contacting us. Please tell us why you are here: \nType '1' if you need help with an order, \nType '2' if you would like to leave feedback, \nType '3' if you have a question about a product."
    handlers = {}
    waiting = collections.deque()
    host = 'localhost'
    port = 8888
    running = True