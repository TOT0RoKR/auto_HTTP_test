
if [ -z $1 ]; then
	echo "please put number of cpus"
	echo "$0 {number of cpus} [number of pinning threads]"
	exit
fi

if [ -z $2 ]; then
	echo "not pinning"
	load=0
else
	echo "$2 thread pinning"
	load=$2
fi


if [ $1 -lt 1 ]; then
	echo "Couldn't number of cpus be under 1"
	exit
fi

if [ $1 -gt 18 ]; then
	echo "Couldn't number of cpus be over 18"
	exit
fi

nr_core=`expr $1 - 1`

for i in `seq 1 $nr_core`
do
	path="/sys/devices/system/cpu/cpu`expr $i`/online"
	echo $path" on"
	echo 1 > $path
done

for i in `seq $1 17`
do
	path="/sys/devices/system/cpu/cpu`expr $i`/online"
	echo $path" off"
	echo 0 > $path
done

echo "smp affinity"
/home/wyldecat/autotest/ixgbe-queue-irq-affinity.sh $nr_core

if [ $load -eq 0 ]; then
	echo "worker_processes ${1};" > /etc/nginx/worker_processes.conf
	echo "" > /etc/nginx/worker_cpu_affinity.conf
else
	echo "worker_processes `expr ${load} \* ${1}`;" > /etc/nginx/worker_processes.conf
	core_index=$(shif=1; for i in `seq 0 $nr_core`; do echo "obase=2; $shif" | bc | xargs printf "%018d "; shif=`expr $shif '*' 2`; done)
	affinity="worker_cpu_affinity$(for j in `seq 1 $load`; do echo $core_index | xargs printf " %s"; done);"
	echo "$affinity" > /etc/nginx/worker_cpu_affinity.conf
fi

service nginx restart
echo "nginx restart"

echo "finished"
