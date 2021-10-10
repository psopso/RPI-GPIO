import time as t
import smbus
import sys

DEVICE_BUS = 1

bus = smbus.SMBus(DEVICE_BUS)

def switch_on(device, ind, momentary):
  bus.write_byte_data(device, ind, 0xFF)

def switch_off(device, ind, momentary):
  bus.write_byte_data(device, ind, 0x00)

def switch_is_on(device, ind):
  if bus.read_byte_data(device, ind) == 255 :
    return True
  else:
    return False
