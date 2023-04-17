set terminal png size 600
set output "reporte_1000_10.png"
set title "1000 peticiones, 10 peticiones concurrentes"
set size ratio 0.6
set grid y
set xlabel "Nro Peticiones"
set ylabel "Tiempo de respuesta (ms)"
plot "output_1000_10.csv" using 9 smooth sbezier with lines title "http://ip_servidor/cipher"