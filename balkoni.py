import spidev
import time
import os
import rrdtool

# Open SPI bus 0
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# Open SPI bus 1
out = spidev.SpiDev()
out.open(0,1)

pump_status_path = '/home/balkoni/pump_status'
pump_on_time = 60*10
rrd_file = '/home/balkoni/balkoni.rrd'
wetness_value = 60

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertVolts(data):
  return (data * 3300.0) / 1024.0

def Temp(channel):
  level = ReadChannel(channel)
  volts = ConvertVolts(level)
  return (volts - 100)/10.0 - 40

def Wetness(channel):
  level = ReadChannel(channel)
  volts = ConvertVolts(level)
  return -0.07 * volts + 197.16

def PumpStatus():
  with file(pump_status_path) as f:
    return f.read().strip()

def SetPumpStatus(value):
  with file(pump_status_path, 'w') as f:
    return f.write(value)

def CheckWetness():
  if Wetness(2) < wetness_value:
    print 'einschalten'
    SetPumpStatus('1')

def CheckTurnOff():
  if PumpStatus() == '1' and os.path.getmtime(pump_status_path) + pump_on_time < time.time():
    print 'ausschalten'
    SetPumpStatus('0')

def SetPumpRelais():
  if PumpStatus() == '1':
    out.xfer2([1])
  else:
    out.xfer2([0])

def UpdateRDD():
  temp1 = Temp(0)
  temp2 = Temp(1)
  wetness = Wetness(2)
  pump_status = PumpStatus()

  rrdtool.update(rrd_file, '-t', 'temp1:temp2:wetness1:pump_status', '--', "N:%s:%s:%s:%s" % (temp1, temp2, wetness, pump_status))