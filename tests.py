from message import Message

# Test a message exchange
test_message_a = Message("TEST", "Hello World!")
a_packed = test_message_a.pack()
a_unpacked, a_leftover = Message.parse(a_packed)
assert(len(a_unpacked) == 1)
assert(a_unpacked[0].message_type == "TEST")
assert(a_unpacked[0].content == "Hello World!")
assert(a_leftover == b"")

# Test leftovers after message
b_unpacked, b_leftover = Message.parse(a_packed + b"NO")
assert(len(b_unpacked) == 1)
assert(b_unpacked[0].message_type == "TEST")
assert(b_unpacked[0].content == "Hello World!")
assert(b_leftover == b"NO")

# Test two messages
test_message_c = Message("TST2", "Hello Planet!")
c_packed = test_message_c.pack()
c_unpacked, c_leftover = Message.parse(a_packed + c_packed)
assert(len(c_unpacked) == 2)
assert(c_unpacked[0].message_type == "TEST")
assert(c_unpacked[0].content == "Hello World!")
assert(c_unpacked[1].message_type == "TST2")
assert(c_unpacked[1].content == "Hello Planet!")
assert(c_leftover == b"")

# Test two messages + leftovers
d_unpacked, d_leftover = Message.parse(a_packed + c_packed + b"NO")
assert(len(d_unpacked) == 2)
assert(d_unpacked[0].message_type == "TEST")
assert(d_unpacked[0].content == "Hello World!")
assert(d_unpacked[1].message_type == "TST2")
assert(d_unpacked[1].content == "Hello Planet!")
assert(d_leftover == b"NO")

# Test lengthy leftovers
e_unpacked, e_leftover = Message.parse(a_packed + b"THESE ARE VERY LONG LEFTOVERS THAT MAKE NO SENSE")
assert(len(e_unpacked) == 1)
assert(e_unpacked[0].message_type == "TEST")
assert(e_unpacked[0].content == "Hello World!")
assert(e_leftover == b"THESE ARE VERY LONG LEFTOVERS THAT MAKE NO SENSE")

# Test partial message
f_unpacked, f_leftover = Message.parse(a_packed[:7])
assert(len(f_unpacked) == 0)
assert(f_leftover == a_packed[:7])

# Test full and partial message
g_unpacked, g_leftover = Message.parse(c_packed + a_packed[:7])
assert(len(g_unpacked) == 1)
assert(g_unpacked[0].message_type == "TST2")
assert(g_unpacked[0].content == "Hello Planet!")
assert(g_leftover == a_packed[:7])