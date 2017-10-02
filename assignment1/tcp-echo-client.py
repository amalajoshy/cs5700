# This example is using Python 3.6
import socket
import sys

# Specify server name and port number to connect to.
#
# API: gethostname()
#   returns a string containing the hostname of the
#   machine where the Python interpreter is currently
#   executing.
server_name = socket.gethostname()
print('Hostname: ', server_name)
server_port = 8181

# Make a TCP socket object.
#
# API: socket(address_family, socket_type)
#
# Address family
#   AF_INET: IPv4
#   AF_INET6: IPv6
#
# Socket type
#   SOCK_STREAM: TCP socket
#   SOCK_DGRAM: UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server machine and port.
#
# API: connect(address)
#   connect to a remote socket at the given address.
s.connect((server_name, server_port))
print('Connected to server ', server_name)

# messages to send to server.
message = ["1+-32/2-4", "5*2+3*2+50-20/2"]

# Send messages to server over socket.
#
# API: send(bytes)
#   Sends data to the connected remote socket.  Returns the number of
#   bytes sent. Applications are responsible for checking that all
#   data has been sent
#
# API: recv(bufsize)
#   Receive data from the socket. The return value is a bytes object
#   representing the data received. The maximum amount of data to be
#   received at once is specified by 'bufsize'.
#
# API: sendall(bytes)
#   Sends data to the connected remote socket.  This method continues
#   to send data from string until either all data has been sent or an
#   error occurs.
bufsize = 1024

def generate_client_msg(msg_array):
	if len(msg_array) == 0:
		raise 'Invalid msg'

	num_of_expressions = len(msg_array)
	message = bytearray()
	message.extend(num_of_expressions.to_bytes(2, byteorder = 'big')) # total number of expressions
	for expr in msg_array:
		expr_byte_str = str.encode(expr)
		message.extend(len(expr_byte_str).to_bytes(2, byteorder = 'big'))
		message.extend(expr_byte_str)
	return message

client_msg = generate_client_msg(message)

s.sendall(client_msg)
data = s.recv(2)
if not data:
 	s.close()
 	sys.exit(1)

num_of_results = int.from_bytes(data, byteorder = 'big')
i = 0
while i < num_of_results:
	data = s.recv(2)
	if not data:
		s.close()
		sys.exit(1)
	expression_size = int.from_bytes(data, byteorder = 'big')
	data = s.recv(expression_size)
	if not data:
		s.close()
		sys.exit(1)
	expression = bytes.decode(data)
	print('Client received: ', expression)

# Close socket to send EOF to server.
s.close()
