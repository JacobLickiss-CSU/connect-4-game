import sys
import selectors
import json
import io
import struct

class Manager:
    def __init__(self, selector, sock, address):
        self.selector = selector
        self.sock = sock
        self.address = address
        self._read_buffer = b""
        self._write_buffer = b""
        self.log = False


    def process(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()


    def _mode_read(self):
        self.selector.modify(self.sock, selectors.EVENT_READ, data=self)


    def _mode_write(self):
        self.selector.modify(self.sock, selectors.EVENT_WRITE, data=self)


    def _mode_readwrite(self):
        self.selector.modify(self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=self)


    def schedule_message(self, message):
        if(self.log):
            print("(" + str(self.address) + ") " + "Writing to buffer: " + str(message))
        self._write_buffer += message


    def _do_read(self):
        self.pre_read()
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._read_buffer += data
                if(self.log):
                    print("(" + str(self.address) + ") " + "Received data: " + str(data))
            else:
                raise RuntimeError("Connection closed.")
        self.post_read()


    def _do_write(self):
        self.pre_write()
        if self._write_buffer:
            try:
                # Should be ready to write
                sent = self.sock.send(self._write_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._write_buffer = self._write_buffer[sent:]
        self.post_write()


    def read(self):
        self._do_read()


    def write(self):
        self._do_write()


    def pre_read(self):
        pass


    def post_read(self):
        pass


    def pre_write(self):
        pass


    def post_write(self):
        pass


    def close(self):
        print("Closing connection to", self.address)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print("Exception in closing connection for ", f"{self.address}: {repr(e)}")
