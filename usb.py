import RPi.GPIO as GPIO
import time
import subprocess
import os

GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

print "PIR Module Test (CTRL+C to exit)"
time.sleep(2)
print "Ready"

for num in range(1,5):
    proc = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE)
    (out,err) = proc.communicate()
    ip = out[0:10+num]
    print(num)
    print(ip)
    cmd = "touch "+ip+".jpg"
    os.system(cmd)
    send_cmd = "/home/pi/dropbox_uploader.sh upload "+ip+".jpg"+" "+"/TDCMakerSpaceCamera/"+ip+".jpg"
    os.system(send_cmd)
    time.sleep(1)

