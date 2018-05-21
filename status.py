#!/usr/bin/python

import balkoni

print "================"
print "Temp1:      %s" % balkoni.Temp(0), balkoni.ConvertVolts(balkoni.ReadChannel(0))
print "Temp2:      %s" % balkoni.Temp(1), balkoni.ConvertVolts(balkoni.ReadChannel(1))
print "Wetness:    %s" % balkoni.Wetness(2), balkoni.ConvertVolts(balkoni.ReadChannel(2))
print "PumpStatus: %s" % balkoni.PumpStatus()
print "================"