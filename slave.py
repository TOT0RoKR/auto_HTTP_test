import communication as cm

socket = cm.open_slave("10.0.0.201", 20200)

while True:
    master = cm.connect_to_master(socket)

    while True:
        data = cm.data_recv(master, 100)

        if not data:
            break

        print('Recv', data)

        cm.data_send(master, data)

        print('Send', data)

    master.close()

