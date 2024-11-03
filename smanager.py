import sys
import selectors
import socket
import json
import io
import struct

import servermatch
import connectionmanager
from gamestate import GameState
from message import Message
from playerstate import PlayerState

class ServerManager(connectionmanager.Manager):
    def __init__(self, selector, sock, address):
        super().__init__(selector, sock, address)
        self.player = PlayerState()
        self.game_state = None
        self.log = True

    def post_read(self):
        # Read messages from the buffer
        if(self._read_buffer):
            messages, self._read_buffer = Message.parse(self._read_buffer)
            # Apply those messages to the player state
            for message in messages:
                self.player.apply_message(message)
            # Apply those messages to the game state
            if(self.game_state is not None):
                for message in messages:
                    self.game_state.apply_message_server(message, self)
            else:
                if(self.match_ready()):
                    self.schedule_message(Message(Message.WAIT, "0").pack())
                    servermatch.assign_game(self)


    def match_ready(self):
        return self.player.match_ready()    
            

    def match_made(self, game_state):
        self.game_state = game_state
        self.schedule_message(Message(Message.PLAY, "1").pack())
        self.schedule_message(Message(Message.INFO, self.game_state.get_player_symbol(self)).pack())
        self.game_state.send_opponent_player(self)
        self.game_state.broadcast_board(self)
        self.schedule_message(Message(Message.TURN, GameState.A).pack())


    def match_ended(self, reason = "None."):
        self.game_state = None
        self.schedule_message(Message(Message.OVER, reason).pack())


    def close(self):
        super().close()
        servermatch.game_disconnect(self, "Disconnected.")
