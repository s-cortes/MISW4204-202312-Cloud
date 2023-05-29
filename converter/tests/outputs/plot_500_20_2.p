set terminal png size 600
set output "output_500_20_2.png"
set title "500 Requests, 20 Concurrent Requests, Attempt 2"
set size ratio 0.6
set grid y
set xlabel "Num. Requests"
set ylabel "Response Time (ms)"
plot "output_500_20_2.csv" using 9 smooth sbezier with lines title "http://ip_servidor/cipher"