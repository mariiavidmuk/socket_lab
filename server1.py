import select
import socket

global dat
SERVER = ('localhost', 8686)
global array
array = []
global res
res = 0
MAX = 10
input = list()
output = list()


def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(SERVER)
    server.listen(MAX)

    return server


def accept_clients(readables, server):
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            input.append(connection)
            print("new connection from {address}".format(address=client_address))
        else:
            data = ""
            try:
                global array
                data = resource.recv(1024)
                data = data.decode("utf-8")
                array.append(data)
                a = ""
                for i in range(len(array)):
                    a += array[i]
                print(a)
                if len(a) == 5:
                    x = ""
                    y = ""
                    oper = a[a.index('.') + 1]
                    global res
                    for k in range(a.index(',')):
                        x += a[k]
                    x = int(x)
                    for m in range(a.index(',') + 1, a.index('.')):
                        y += a[m]
                    y = int(y)
                    if oper == "+":
                        res = x + y
                    if oper == "-":
                        res = x - y
                    if oper == "*":
                        res = x * y
                    if oper == "/":
                        res = x / y
                    if res == 0:
                        resource.send(str(res).encode())
                    x = ""
                    y = ""
                    array = []
                if len(array) > 5:
                    array = []
            except ConnectionResetError:
                pass

            if data:

                if resource not in output:
                    output.append(resource)


            else:

                delete(resource)


def delete(resource):
    if resource in output:
        output.remove(resource)
    if resource in input:
        input.remove(resource)
    resource.close()

    print('closing connection ' + str(resource))


def send_result(writables):
    for resource in writables:
        try:
            global res
            if res != 0:
                global array
                resource.send(str(res).encode())
                res = 0
                array = []
        except OSError:
            delete(resource)


if __name__ == '__main__':
    server = create_server()
    input.append(server)
    try:
        while input:
            read, write, exception = select.select(input, output, input)
            accept_clients(read, server)
            send_result(write)
    except KeyboardInterrupt:
        delete(server)
