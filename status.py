#!/usr/bin/python

from balkoni import Balkoni

balkoni = Balkoni()

print "================"
print "Temp1:      %s" % balkoni.temp1
print "Temp2:      %s" % balkoni.temp2
print "Wetness:    %s" % balkoni.wetness
print "PumpStatus: %s" % balkoni.pump_status()
print "================"