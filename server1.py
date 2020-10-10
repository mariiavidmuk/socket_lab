import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()
array = []
while True:
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
