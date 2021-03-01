if [ -z $1 ]; then
	i=17
fi
cores=$(expr 50 + $1)

echo "number:50~67 /proc/irq/[number]/smp_affinity exchange"

shif=1
i=50
while [ $i -le 67 ]; do
	path="/proc/irq/$i/smp_affinity"

	echo "obase=16; $shif" | bc > $path
	shif=$(expr $shif \* 2)

	cat $path | xargs echo "$i"

	i=$(expr $i + 1)
	temp=$(expr $i - 50)
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
