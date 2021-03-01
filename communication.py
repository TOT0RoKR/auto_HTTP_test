import socket as sk


def open_slave(ip, port):
    PORT = port
    HOST = ip

    socket = sk.socket(sk.AF_INET, sk.SOCK_STERAM)

    socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    socket.bind((HOST, PORT))

    socket.listen()

    return socket


def connect_to_master(socket):
    master, _ = socket.accept()

    return master


def connect_to_slave(ip, port):
    socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    socket.connect((ip, port))

    return socket


def data_recv(socket, size):
    data = socket.recv(size)

    if not data:
        return data, 0


def data_send(socket, data):
    data = "{:<10}".format(data)
    socket.sendall(data)

