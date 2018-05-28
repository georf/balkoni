import spidev
import time
import os
import rrdtool
import time

pump_status_path = '/home/balkoni/pump_status'
pump_on_time = 60*15
rrd_file = '/home/balkoni/balkoni.rrd'
wetness_value = 70

class Balkoni:
  def __init__(self):
    # Open SPI bus 0
    self.spi_in = spidev.SpiDev()
    self.spi_in.open(0,0)
    self.spi_in.max_speed_hz=1000000

    # Open SPI bus 1
    self.spi_out = spidev.SpiDev()
    self.spi_out.open(0,1)

    self.wetness = self.wetness_normalized(2)
    self.temp1 = self.temp_normalized(0)
    self.temp2 = self.temp_normalized(1)

  def read_channel(self, channel):
    adc = self.spi_in.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

  def convert_volts(self, data):
    return (data * 3300.0) / 1024.0

  def temp_of(self, channel):
    time.sleep(0.01)
    level = self.read_channel(channel)
    volts = self.convert_volts(level)
    return (volts - 100)/10.0 - 40

  def temp_normalized(self, channel):
    values = list(map((lambda x: self.temp_of(channel)), range(5)))
    return sum(values) / len(values)

  def wetness_of(self, channel):
    time.sleep(0.01)
    level = self.read_channel(channel)
    volts = self.convert_volts(level)
    return -0.07 * volts + 197.16

  def wetness_normalized(self, channel):
    values = list(map((lambda x: self.wetness_of(channel)), range(5)))
    return sum(values) / len(values)

  def pump_status(self):
    with file(pump_status_path) as f:
      return f.read().strip()

  def set_pump_status(self, value):
    with file(pump_status_path, 'w') as f:
      return f.write(value)

  def check_wetness(self):
    if self.wetness < wetness_value:
      self.set_pump_status('1')

  def check_turn_off(self):
    if self.pump_status() == '1' and os.path.getmtime(pump_status_path) + pump_on_time < time.time():
      self.set_pump_status('0')

  def set_pump_relais(self):
    if self.pump_status() == '1':
      self.spi_out.xfer2([1])
    else:
      self.spi_out.xfer2([0])

  def update_rdd(self):
    rrdtool.update(rrd_file, '-t', 'temp1:temp2:wetness1:pump_status', '--', "N:%s:%s:%s:%s" % (self.temp1, self.temp2, self.wetness, self.pump_status()))
