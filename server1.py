import socket
import threading
sock = socket.socket()
sock.bind(('', 123))
sock.listen(1)
global conn
def recieve():
    array = []
    while True:
        global conn
        data = conn.recv(1024)
        data = data.decode("utf-8")
        array.append(data)
        x = 0
        if len(array) == 3:
            if array[2] == '+':
                x = int(array[0]) + int(array[1])
            if array[2] == '-':
                x = int(array[0]) - int(array[1])
            if array[2] == '*':
                x = int(array[0]) * int(array[1])
            if array[2] == '/':
                x = int(array[0]) / int(array[1])
            print(x)
            conn.send(str(x).encode())
            array = []
        if not data:
            break
    conn.close()


def accept_clients():
    while True:
        global sock
        global conn
        (conn, address) = sock.accept()
        rT = threading.Thread(target=recieve)
        rT.start()
        rT.join()

accept_clients()