#  subprocess.call('/home/wyldecat/Fastset-no-option.sh', shell=True)

CONFFILENAME = "machine_test.conf"

with open(CONFFILENAME, mode='rt') as f:
    lines = f.readlines()

import subprocess # shell exec
import communication as cm
import time
import os

def current_time_fn():
    return time.strftime('%y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    #  return time.strftime('%x %X', time.localtime(time.time()))

DIRECTORYNAME = "machine_test_results/" + current_time_fn() + "/"
try:
    if not(os.path.isdir(DIRECTORYNAME)):
        os.makedirs(os.path.join(DIRECTORYNAME))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

LOGFILENAME = DIRECTORYNAME + "all.log"


def print_log(*args):
    current_time = current_time_fn() + "  "
    with open(LOGFILENAME, mode='at') as f:
        f.writelines(current_time + " ".join(map(str, args)) + "\n")
    print(current_time, *args)

slaves = []

STATES = ["down", "online", "loaded", "running", "finished"]
master_ip = "127.0.0.1"
port = -1

master_cores = 9
path = "index0.html"
tests = []

mpstat = False

line_nr = 0
for line in lines:
    line_nr += 1
    line = line[:-1]
    #  print_log(line)
    config = line.split()

    if config is None or config[0] is None:
        continue

    elif config[0][0] == "#": # comments
        continue

    elif config[0] == "master": # set master ip
        if len(config) != 2:
            print_log("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        master_ip = config[1]
        #  master_cores = config[2]
        #  subprocess.call('/home/wyldecat/machinetest/cpu_hotplug_nginx.sh {0}'.format(master_cores), shell=True)
        print_log("master: ", master_ip)
        #  time.sleep(2)

    elif config[0] == "test": # set tests
        if len(config) != 6:
            print_log("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        test = {"times":int(config[1]), "cores":int(config[2]), "path":config[3],
                "duration":config[4], "connections":int(config[5])}
        tests.append(test)
        print_log(test)

    elif config[0] == "port": # set port num(slaves)
        if len(config) != 2:
            print_log("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        port = int(config[1])
        print_log("port: ", port)

    elif config[0] == "slave": # slave add
        if len(config) != 3:
            print_log("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        slave = {"ip":config[1], "threads":int(config[2]), "state":"down", "socket":None}
        slaves.append(slave)
        print_log(slave)

    elif config[0] == "mpstat": # mpstat
        if len(config) != 1:
            print_log("FieldError(", line_nr, "): ", CONFFILENAME)
            exit()
        mpstat = True

    else:
        print_log("SyntaxError(", line_nr, "): ", CONFFILENAME)
        exit()

if port < 1024 or port > 65535:
    print_log("Unavailable Port: ", port)
    exit()


# connect to slaves
for slave in slaves:
    print_log('set slave ', slave['ip'])
    socket = cm.connect_to_slave(slave['ip'], port)
    slave['socket'] = socket
    #  cm.data_send(socket, "connect {0} {1} {2} {3}".format())
    #  ret = cm.data_recv(socket, 100)
    cm.data_send(socket, "on {0}".format(slave['threads']))
    ret = cm.data_recv(socket, 100).split()
    #  print (ret)
    if ret[0] == "success":
        slave['state'] = "online"
    #  slave['state'] = "online"

# online check
for slave in slaves:
    if slave['state'] != "online":
        print_log("Not connected with slave:", slave['ip'])
        exit()
        

# test start
for test in tests:
    subprocess.call('/home/wyldecat/machinetest/cpu_hotplug_nginx.sh {0}'.format(test['cores']), shell=True)
    time.sleep(2)
    for slave in slaves:
        socket = slave['socket']
        cm.data_send(socket, "load {0} {1} {2}".format(test['path'],
            test['duration'], test['connections']))
        ret = cm.data_recv(socket, 100).split()
        if ret[0] == "success":
            slave['state'] = "loaded"
            print_log("loaded", slave['ip'])

    for i in range(test['times']):
        print_log("test start(", i, "):", test)
        if mpstat is True:
            mpstat_fd = open(DIRECTORYNAME + "mpstat{0}_{1}_{2}_{3}".format(i,
                test['cores'], test['path'], test['duration'], test['connections']), mode='wt')
            mpstat_process = subprocess.Popen('mpstat 1',
                stdout=mpstat_fd, stderr=mpstat_fd, shell=True)

        for slave in slaves:
            socket = slave['socket']
            cm.data_send(socket, "run")
            slave['state'] = "running"
            print_log("run", slave['ip'])

        for slave in slaves:
            socket = slave['socket']
            ret = cm.data_recv(socket, 100).split()
            #  print (ret)
            if ret is not None and ret[0] == "success":
                slave['state'] = "finished"
                print_log("finished", slave['ip'])
            else:
                print_log("Don't run:", slave['ip'])
                exit()


        for slave in slaves:
            socket = slave['socket']
            cm.data_send(socket, "finish")
            ret = cm.data_recv(socket, 65535)
            #  print (ret)
            with open(DIRECTORYNAME + "result{0}_{1}_{2}_{3}_{4}".format(i, \
                test['cores'], test['path'], test['duration'],
                test['connections'], slave['ip']) \
                , mode='wt') as f:
                f.write(ret)
            slave['state'] = "loaded"
            print_log("loaded", slave['ip'])

        if mpstat is True:
           mpstat_process.kill()
           #  mpstat_process.terminate()
           mpstat_fd.close()

print_log ("end")
