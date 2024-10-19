import sys
import selectors
import socket
import json
import io
import struct

import connectionmanager
from gamestate import GameState
from message import Message
from playerstate import PlayerState

class ClientManager(connectionmanager.Manager):
    def __init__(self, selector, sock, address):
        super().__init__(selector, sock, address)
        self.player = PlayerState()
        self.state = GameState()

    def post_read(self):
        # Read messages from the buffer
        if(self._read_buffer):
            messages, self._read_buffer = Message.parse(self._read_buffer)
            # Handle some messages in the manager
            for message in messages:
                if(message.message_type == Message.OVER):
                    print("The game has ended! Reason: " + message.content)
                    self.close()
            # Apply those messages to the game state
            for message in messages:
                self.state.apply_message_client(message)
