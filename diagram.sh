#!/bin/bash

for i in -12h -24h -7d -30d -90d -360d; do

  rrdtool graph www/balkoni$i.png -w 1270 -h 400 -t "Balkon $i" \
  --end now --start end$i \
  --vertical-label 'degree' \
  --right-axis-label 'percent' --right-axis 2:0 \
  DEF:temp1=balkoni.rrd:temp1:AVERAGE \
  VDEF:temp1avg=temp1,AVERAGE \
  DEF:wetness1=balkoni.rrd:wetness1:AVERAGE \
  CDEF:wetness1_scaled=wetness1,0.5,* \
  VDEF:wetnessavg=wetness1_scaled,AVERAGE \
  DEF:pump_status=balkoni.rrd:pump_status:AVERAGE \
  CDEF:pump_status_scaled=pump_status,50,* \
  "AREA:pump_status_scaled#00ff11:Pumpe \n" \
  "LINE:temp1avg#AEB6FF80" \
  "LINE:temp1#7280FF:Temperatur" \
  "GPRINT:temp1:MIN:Min %6.2lf%s°C " \
  "GPRINT:temp1:MAX:Max %6.2lf%s°C " \
  "GPRINT:temp1:AVERAGE:Average %6.2lf%s°C " \
  "GPRINT:temp1:LAST:Current %6.2lf%s°C\n" \
  "LINE:wetnessavg#AF887580" \
  "LINE:wetness1_scaled#AF5023:Feuchte   " \
  "GPRINT:wetness1:MIN:Min %6.2lf %%  " \
  "GPRINT:wetness1:MAX:Max %6.2lf %%  " \
  "GPRINT:wetness1:AVERAGE:Average %6.2lf %%  " \
  "GPRINT:wetness1:LAST:Current %6.2lf %%\n"
done
