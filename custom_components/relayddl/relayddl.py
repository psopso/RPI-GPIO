import time as t
import smbus
import sys

DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)

def pokus():
  for i in range(1,5):
    bus.write_byte_data(DEVICE_ADDR, i, 0xFF)
    t.sleep(1)
    bus.write_byte_data(DEVICE_ADDR, i, 0x00)
    t.sleep(1)

def switch_on(device, pin):
  bus.write_byte_data(device, pin, 0xFF)

def switch_off(device, pin):
  bus.write_byte_data(device, pin, 0x00)

def switch_is_on(device, pin):
  if bus.read_byte_data(device, pin) == 255 :
    return True
  else:
    return False
