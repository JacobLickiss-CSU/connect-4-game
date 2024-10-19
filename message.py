import struct

class Message:
    version = 1
    header_format = ">i4si"

    CHAT = "CHAT"
    NAME = "NAME"
    MOVE = "MOVE"
    INFO = "INFO"
    PLAY = "PLAY"
    RSLT = "RSLT"
    WAIT = "WAIT"
    OVER = "OVER"

    def __init__(self, message_type, content):
        # Message type - A four byte string which indicates the purpose of the message
        self.message_type = message_type
        # Content - A variable length string which contains the actual message
        self.content = content

    def pack(self):
        # Convert the message content into the body
        body = bytes(self.content, encoding="utf-8")
        # Determine the length
        length = len(body)
        # Create the header
        header = struct.pack(Message.header_format, Message.version, bytes(self.message_type, encoding="utf-8"), length)
        # Create the body
        body_format = ">{0}s".format(length)
        packed_body = struct.pack(body_format, body)
        # Return the result
        return header + packed_body
        

    @staticmethod
    def parse(data):
        # Calculate the header size
        header_size = struct.calcsize(Message.header_format)
        # Prepare the result messages array
        messages = []
        # Prepare a data index
        index = 0

        # Loop until all messages have been processed
        while(len(data) - index > header_size):
            # Grab a header
            header = data[index:index + header_size]
            index += header_size
            in_version, in_type, in_length = struct.unpack(Message.header_format, header)
            # Check if we have all the data we're supposed to
            if(len(data) < index + in_length):
                index -= header_size
                break
            # Get the body
            body_data = data[index:index + in_length]
            index += in_length
            body_format = ">{0}s".format(in_length)
            in_body = struct.unpack(body_format, body_data)[0]
            # Decode the body
            body = in_body.decode('utf-8')
            # Decode the type
            message_type = in_type.decode('utf-8')
            messages.append(Message(message_type, body))


        # Return all the messages found, and leftover data
        return (messages, data[index:])