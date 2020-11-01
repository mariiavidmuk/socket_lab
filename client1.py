import socket

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8686))
        x = int(input("Enter the first number: "))
        x = bytes(str(x), "utf-8")
        y = int(input("Enter the second number: "))
        y = bytes(str(y), "utf-8")
        oper = input("Enter the operation: ")
        if oper != '+' and oper != '-' and oper != '*' and oper != '/':
            print("Wrong input")
            sock.close()
        oper = bytes(oper, "utf-8")
        divisioner = ','
        divisioner = bytes(str(divisioner), "utf-8")
        division = '.'
        division = bytes(str(division), "utf-8")
        sock.send(x)
        sock.send(divisioner)
        sock.send(y)
        sock.send(division)
        sock.send(oper)
        result = sock.recv(1024).decode()
        print("The answer is:", result)
    except:
        print("Wrong input")
        break
