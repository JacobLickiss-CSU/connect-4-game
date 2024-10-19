
from message import Message

class PlayerState:
    def __init__(self):
        self.name = None

    def apply_message(self, message):
        match message.message_type:
            case Message.NAME:
                self.name = message.content
                print("Name registered: " + self.name)

    def match_ready(self):
        return self.name != None