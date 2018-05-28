#!/usr/bin/python

from balkoni import Balkoni

balkoni = Balkoni()
balkoni.check_wetness()
balkoni.check_turn_off()
balkoni.set_pump_relais()

balkoni.update_rdd()