import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
while (True):
    try:
        x = input("Enter the first number: ")
        x = bytes(x, "utf-8")
        y = input("Enter the second number: ")
        y = bytes(y, "utf-8")
        oper = input("Enter the operation: ")
        oper = bytes(oper, "utf-8")
        sock.send(x)
        sock.send(y)
        sock.send(oper)
        result = sock.recv(1024).decode()
        print("The answer is:", result)

    except:
        sock.close()
