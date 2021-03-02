#  import subprocess # shell exec
#  subprocess.call('/home/wyldecat/Fastset-no-option.sh', shell=True)

CONFFILENAME = "machine_test.conf"

with open(CONFFILENAME, mode='rt') as f:
    lines = f.readlines()

import communication as cm

slaves = []

STATES = ["down", "online", "loaded", "running", "finished"]
master_ip = "127.0.0.1"
port = -1

line_nr = 0
for line in lines:
    line_nr += 1
    line = line[:-1]
    #  print(line)
    config = line.split()

    if config[0][0] == "#": # comments
        continue
    elif config[0] == "master": # set master ip
        if len(config) != 2:
            print("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        master_ip = config[1]
        print("master:", master_ip)
    elif config[0] == "port": # set port num(slaves)
        if len(config) != 2:
            print("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        port = int(config[1])
        print("port:", port)
    elif config[0] == "slave": # slave add
        if len(config) != 6:
            print("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        slave = {"ip":config[1], "path":config[2], "duration":config[3],
                "threads":config[4], "connections":config[5], "state":"down",
                "socket":None}
        slaves.append(slave)
        print(slave)
    else:
        print("SyntaxError(", line_nr, "):", CONFFILENAME)
        exit()

if port < 1024 or port > 65535:
        print("Unavailable Port(", line_nr, "):", CONFFILENAME)
        exit()


# connect to slaves
for slave in slaves:
    socket = cm.connect_to_slave(slave['ip'], port)
    slave['socket'] = socket
    slave['state'] = "online"
    cm.data_send(socket, "asdasd")
    print('send')
    cm.data_recv(socket, 100)
    print('recv')



print ("end")
