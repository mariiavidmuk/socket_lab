import select
import socket

global dat
SERVER_ADDRESS = ('localhost', 8686)
global array
array = []
global res
res = 0
# Говорит о том, сколько дескрипторов единовременно могут быть открыты
MAX_CONNECTIONS = 10

# Откуда и куда записывать информацию
INPUTS = list()
OUTPUTS = list()


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(SERVER_ADDRESS)
    server.listen(MAX_CONNECTIONS)

    return server


def handle_readables(readables, server):
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            INPUTS.append(connection)
            print("new connection from {address}".format(address=client_address))
        else:
            data = ""
            try:
                global array
                data = resource.recv(1024)
                data = data.decode("utf-8")
                array.append(data)
                print(array)
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

                    array = []
            except ConnectionResetError:
                pass

            if data:

                if resource not in OUTPUTS:
                    OUTPUTS.append(resource)


            else:

                clear_resource(resource)


def clear_resource(resource):
    if resource in OUTPUTS:
        OUTPUTS.remove(resource)
    if resource in INPUTS:
        INPUTS.remove(resource)
    resource.close()

    print('closing connection ' + str(resource))


def handle_writables(writables):
    for resource in writables:
        try:
            global res
            resource.send(str(res).encode())

            res= 0
        except OSError:
            clear_resource(resource)


if __name__ == '__main__':
    server_socket = get_non_blocking_server_socket()
    INPUTS.append(server_socket)

    print("server is running, please, press ctrl+c to stop")
    try:
        while INPUTS:
            readables, writables, exceptional = select.select(INPUTS, OUTPUTS, INPUTS)
            handle_readables(readables, server_socket)
            handle_writables(writables)
    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Server stopped! Thank you for using!")
