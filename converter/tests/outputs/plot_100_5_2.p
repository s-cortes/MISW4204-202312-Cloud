set terminal png size 600
set output "output_100_5_2.png"
set title "100 Requests, 5 Concurrent Requests, Second Attempt"
set size ratio 0.6
set grid y
set xlabel "Num. Requests"
set ylabel "Response Time (ms)"
plot "output_100_5_2.csv" using 9 smooth sbezier with lines title "http://ip_servidor/cipher"
