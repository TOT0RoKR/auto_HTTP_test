if [ -z $1 ]; then
	i=17
fi
queue=70
cores=$(expr $queue + $1)

echo "number:$queue~$(expr $queue + 17) /proc/irq/[number]/smp_affinity exchange"

shif=1
i=$queue
while [ $i -le $(expr $queue + 17) ]; do
	path="/proc/irq/$i/smp_affinity"

	echo "obase=16; $shif" | bc > $path
	shif=$(expr $shif \* 2)

	cat $path | xargs echo "$i"

	i=$(expr $i + 1)
	temp=$(expr $i - $queue)
	temp=$(expr $temp % $(expr 1 + $1))
	if [ $temp -eq 0 ]; then
		shif=1
	fi
done

# for i in `seq 50 $cores`; do
# 	path="/proc/irq/$i/smp_affinity"
#
# 	echo "obase=16; $shif" | bc > $path
# 	shif=`expr $shif \* 2`
#
# 	cat $path | xargs echo "$i"
#
# done
