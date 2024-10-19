from message import Message

class GameState:
    def __init__(self):
        self.player_a = None
        self.player_b = None
        self.board = [[0 for x in range(7)] for y in range(6)]

    def apply_message_server(self, message):
        match message.message_type:
            case Message.MOVE:
                pass

    def apply_message_client(self, message):
        match message.message_type:
            case Message.WAIT:
                print("Waiting for a match...")
            case Message.PLAY:
                print("Play begins!")
            case Message.MOVE:
                pass