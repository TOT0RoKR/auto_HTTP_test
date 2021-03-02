sysctl -w net.ipv4.tcp_max_tw_buckets="1800000"

sysctl -w net.ipv4.tcp_timestamps="1"
sysctl -w net.ipv4.tcp_tw_reuse="1" # 0->1로 변경. 이부분이 가장 중요. 이것 때문에 좌지 우지 됨.
					# (server를 잘 saturate 함. 1이나 2나 잘 됨)
