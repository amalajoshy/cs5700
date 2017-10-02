# This example is using Python 3.6
import socket
import _thread
import time

# Get host name, IP address, and port number.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

# Make a TCP socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to server IP and port number.
s.bind((host_ip, host_port))

# Start listen to incoming requests.
s.listen()
print('Server started. Waiting for connection...')

# Current time on the server.
def now():
  return time.ctime(time.time())

def log(msg, addr):
  print('Server received: ', msg, ' from ', addr)

bufsize = 1024
def handler(conn, addr):
  try:
    data = conn.recv(2)
    if not data:
      conn.close()
      return

    num_of_expressions = int.from_bytes(data, byteorder = 'big')
    log(num_of_expressions, addr)
    i = 0
    result_array = []
    while i < num_of_expressions:
      data = conn.recv(2)
      if not data:
        break
      expression_size = int.from_bytes(data, byteorder = 'big')
      log(expression_size, addr)

      expression = ""
      bytes_remaining = expression_size
      while bytes_remaining > 0:
        size = min(bytes_remaining, 16)
        expression += bytes.decode(conn.recv(size))
        bytes_remaining -= size
      
      log(expression, addr)

      result_array.append(evaluate(expression))
      i += 1
    
    conn.sendall(generate_response_msg(result_array))
  finally:
    conn.close()

def generate_response_msg(result_array):
  response = bytearray()
  num_of_results = len(result_array)
  response.extend(num_of_results.to_bytes(2, byteorder = 'big')) # total number of results
  for result in result_array:
    result_byte_str = str.encode(str(result))
    response.extend(len(result_byte_str).to_bytes(2, byteorder = 'big'))
    response.extend(result_byte_str)
  return response

def operate(op1, op2, operator):
  if operator == '+':
    return op1 + op2
  elif operator == '-':
    return op1 - op2
  elif operator == '*':
    return op1 * op2
  elif operator == '/':
    return int(op1 / op2)
  else:
    raise "Unsupported operation: " + operator

# Algorithm

# If character exists to be read:

# If character is operand push on the operand stack
# Else if character is operator
# While the top of the operator stack is not of smaller precedence than this character.
# Pop operator from operator stack.
# Pop two operands (op1 and op2) from operand stack.
# Store op1 op op2 on the operand stack back to 2.1.
# Else (no more character left to read):

# Pop operators untill operator stack is not empty.
# Pop top 2 operands and push op1 op op2 on the operand stack.
# return the top value from operand stack.
def evaluate(expression):
  supported_operators = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
  }
  operand_stack = []
  operator_stack = []
  operand_builder = ""

  for c in expression:
    if c in supported_operators:
      if len(operand_builder) != 0:
        try:
          operand = int(operand_builder)
        except ValueError:
          raise "Invalid expression: " + expression
        operand_builder = ""
        operand_stack.append(operand)
        if len(operator_stack) > 0:
          operator_at_top = operator_stack[len(operator_stack) - 1]
          if supported_operators[operator_at_top] >= supported_operators[c]:
            operator_stack.pop()
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            result = operate(op1, op2, operator_at_top)
            operand_stack.append(result)
        operator_stack.append(c)
      elif c == '+' or c == '-':
        operand_builder += c
      else:
        raise "Invalid expression: " + expression

    else:
      operand_builder += c

  if len(operand_builder) != 0:
    try:
      operand = int(operand_builder)
    except ValueError:
      raise "Invalid expression: " + expression
    operand_stack.append(operand)

  while len(operand_stack) > 1:
    op2 = operand_stack.pop()
    op1 = operand_stack.pop()
    operator = operator_stack.pop()
    result = operate(op1, op2, operator)
    operand_stack.append(result)

  return operand_stack.pop()



while True:
  conn, addr = s.accept()
  print('Server connected by', addr, 'at', now())
  _thread.start_new_thread(handler, (conn,addr))
