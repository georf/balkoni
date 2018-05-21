# Balkoni

Auf meinem Balkon stehen seit ein paar Jahren jedes Jahr neue Blumen. Irgendwann im Hochsommer vergesse ich immer sie ein paar Tage zu gießen und schon sind sie vertrocknet. Deshalb wollte ich in diesem Jahr eine automatische Bewässerung bauen.

Die Steuerung wird über ein Raspberry Pi geregelt, der auf dem Balkon steht. Er ließt dabei einen Bodenfeuchtigkeitssensor über einen MCP3008-IC aus und steuert die Pumpe über ein 74HC959-Shirt-Register. Beide Bauteile werden über SPI angesprochen und lauschen in meinem Fall über die Kanäle 0 und 1.

Außerdem wird zur Zeit noch die Temperatur ausgelesen. Ich habe zwei Sensoren (TMP36GT9) verbaut, aber nur einer liefert gute Ergebnisse.

## Allgemeiner Ablauf

Über einen Cronjob werden die Werte ausgelesen. Fällt die Feuchtigkeit unter 60%, wird die Pumpe eingeschaltet. Ist die Pumpe über 10 Minuten an, wird sie wieder ausgeschaltet.

## Visualisierung über rrdtool

Folgende rrd-Datenbank hält die Werte:

```
rrdtool create balkoni.rrd --start now-10d --step 60s \
   DS:temp1:GAUGE:10m:-40:60 \
   DS:temp2:GAUGE:10m:-40:60 \
   DS:wetness1:GAUGE:10m:0:100 \
   DS:wetness2:GAUGE:10m:0:100 \
   DS:pump_status:GAUGE:10m:0:1 \
   RRA:AVERAGE:0.5:1:10d \
   RRA:AVERAGE:0.5:5m:90d \
   RRA:AVERAGE:0.5:1h:10y
```

Jede Minute werden im Cronjob die Werte gespeichert. Alle 5 Minuten werden die Diagramme neu gezeichnet. Über Nginx wird eine einfache Webseite mit den Diagrammen bereitgestellt: https://balkoni.georf.de/
