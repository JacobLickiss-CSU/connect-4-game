import sys
import selectors
import socket
import json
import io
import struct

import connectionmanager

class ServerManager(connectionmanager.Manager):
    
    def post_read(self):
        # For now, print whatever the client sends, and echo
        if(self._read_buffer):
            print("From " + f"{self.address}: {self._read_buffer}")
            self.schedule_message(self._read_buffer)
            self._read_buffer = b""
