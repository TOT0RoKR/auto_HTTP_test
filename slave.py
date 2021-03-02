import communication as cm
import subprocess as sp

socket = cm.open_slave("10.0.0.201", 20200)

path = "index0.html"
duration = "10s"
threads = "1"
connections = "100"

#  RESULTFILE = "res.txt"

while True:
    master = cm.connect_to_master(socket)

    while True:
        text = cm.data_recv(master, 100).split()

        if not text:
            break

        print('Recv', text)

        if text[0] == "run":
            #  result_fd = open(RESULTFILE, mode="wt")
            command = 'wrk_shell.sh {0} {1} {2} {3}'.format(path, duration, threads, connections)
            wrk = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            (out, err) = wrk.communicate()
            print('run')
            print((out + err).decode())
        elif text[0] == "on":
            threads = text[1]
        elif text[0] == "load":
            path = text[1]
            duration = text[2]
            connections = text[3]
        elif text[0] == "finish":
            cm.data_send(master, (out + err).decode())
            continue



        cm.data_send(master, "success")

    master.close()

