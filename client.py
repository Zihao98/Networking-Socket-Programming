'''
Author:                 Zihao Tian
NU ID:                  002131414
Secret Flag:            9474efcc74fbd7acc6c9195a20012c4516088477f79282284cdb4663550787c4
High-level Approach:
The goal of this project is to implement the client-end code, to send/receive data to/from the server.
The client and server communicate with each other by using sockets through TCP protocol.
To start connecting tot he client, server need to send a intro message to the server, while server is
listening (To send data to the server, the client needs to know the address and port of the server and generate
socket stream).
once the server received a correct intro message, it starts to send a math expression for
the client to solve and if the returned answer is correct, it send another one (100 expression totally).
On the client side, once the connection is established, it uses a loop to take and solve 100 expressions
given by the server.
The received message is decoded and the string is split by ' ', the first and third elements
are thr numbers, and the operation is according to the second element. After calculating the expression, the
number is converted to string (with "EECE7374 RSLT " at the beginning)and encoded and sent back to server.
When all the expressions are solved correctly, the secret flag is send to client. We can see the flag on both
server and client side.
'''

import socket

#Constants
server_hostname = 'kopi.ece.neu.edu'
#default_server_port = 5204
buffer_size = 4096
number_of_expressions = 100

#establish the connection with server
'''
ADDR = (server_hostname, default_server_port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
'''
#encode and send message to server
def send(msg):
    message = msg.encode('utf-8')
    client.send(message)

#receive and decode the message sent from server
def receive():
    msg = client.recv(buffer_size)
    print(msg.decode('utf-8'))

#the main process of solving the expressions
def run_client():
    #send the intro message to ask server sending expressions
    send("EECE7374 INTR 002131414")
    print("intro sent\n")

    #receive and solve the expressions for 100 times
    for iteration in range(number_of_expressions):
        for port in range(5203, 5213):
            try:
                default_server_port = port
                ADDR = (server_hostname, default_server_port)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(ADDR)
                #receive the message from server
                math = client.recv(buffer_size)
                print("expression received")
                break;

            except:
                print("Unable to receive expression from server. Switching Server Port...")

        if math:
            ans = 0
            #split the expression into three parts
            math = math.split()
            #two numbers and an operation
            num1 = int(math[2])
            num2 = int(math[4])
            op = math[3].decode('utf-8')

            #determine with eperation to apply
            if op == '+':
                ans = num1 + num2
            if op == '-':
                ans = num1 - num2
            if op == '*':
                ans = num1 * num2
            if op == '/':
                ans = num1 / num2

            #merge the result and header "EECE7374 RSLT"
            print(num1, op, num2)
            res = ["EECE7374", "RSLT", str(ans)]
            res = ' '.join(res)
            #encode the result string and send it back
            send(res)
            print("answer sent")
            print(ans, "\n")
    #after solving all the expression, call receive() to get the flag
    receive()


if __name__ == '__main__':
    run_client()
