# /home/kc/wrk/wrk -t 18 -c 5500  --timeout ${1} --latency -d ${1}s http://60.60.60.10:17500/index.php
# /home/kc/wrk/wrk -t 18 -c 5500  --timeout ${1} --latency -d ${1}s http://10.0.0.210:17500/index0.html
../wrk/wrk -t ${3} -c ${4}  --timeout ${2} --latency -d ${2} http://10.0.0.210:17500/${1}
# /home/kc/wrk/wrk -t 18 -c 5500  --timeout ${1} --latency -d ${1}s http://60.60.60.10:17500/index0.html
# /home/kc/wrk/wrk -t 18 -c 50  --timeout ${1} --latency -d ${1}s http://60.60.60.10:17500/index_shm.php
# for i in `seq 1 5`; do
	# taskset -c $i wrk -t 1 -c 500 --latency -d 10s http://60.60.60.10:17500/index${i}.html &
# done
