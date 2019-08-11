# usr/bin/bash -tt
import os
import glob
import time
import smtplib
import serial
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def sendsms():
    recip = "+212679032603"
    msg="temperature is high"
    phone = serial.Serial("/dev/ttyUSB0",115200,timeout=5)
    try:
        time.sleep(0.5)
        phone.write(b'ATZ\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGS="'+recip.encode()+ b'"\r')
        time.sleep(0.5)
        phone.write(msg.encode()+b"\r")
        time.sleep(0.5)
        phone.write(bytes([26]))
    finally:
        phone.close()
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if temp_c >10:
            sendsms()
        return temp_c
	
while True:
	print(read_temp())
	time.sleep(1)
    
    
    
