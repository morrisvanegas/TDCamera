#!/usr/bin/python
import picamera
import os
import time
import math
import datetime
import RPi.GPIO as GPIO
from time import sleep
from dateutil import tz
from sys import stdout
from datetime import datetime
import subprocess

# get IP address and save it
#proc = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE)
#(out, err) = proc.communicate()
#ip_11 = out[0:11]+".txt"
#ip_12 = out[0:12]+".txt"
#ip_name11 = "touch "+ip_11
#ip_name12 = "touch "+ip_12
#os.system(ip_name11)
#os.system(ip_name12)
#ip_name11_cmd = "/home/pi/dropbox_uploader.sh upload "+ip_11+" OMOAcamera1/ip/"
#ip_name12_cmd = "/home/pi/dropbox_uploader.sh upload "+ip_12+" OMOAcamera1/ip/"
#os.system(ip_name11_cmd)
#os.system(ip_name12_cmd)


camera = picamera.PiCamera()
start_time = time.time()
hour_old = datetime.now().strftime("%H")
path_to_images = '/home/pi/Desktop/capture'
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')
#fecha_old = "2017-01-20"
fecha_old = datetime.now().strftime("%Y-%m-%d")
#loop_time = 10 #add 5 seconds for ./dropbox-uploader and deleting
loop_time = 60
dropbox_name = "TDCMakerSpaceCamera"
#dropbox = input("send thru dropbox (0=no, 1=yes): ")
#dropbox = int(dropbox)
dropbox = 1
#if dropbox==1:
#    loop_time = loop_time-5
#    if loop_time<1:
#        loop_time = 1
print ("frequency is "+str(loop_time)+" seconds (+5 if sending through dropbox)")
#os.system("raspistill -o Desktop/camera/cam.jpg")
#use .replace if time zone of raspi is utc
#date = datetime.now().replace(tzinfo=from_zone).astimezone(to_zone)

# picam documentation: https://www.raspberrypi.org/documentation/usage/camera/python/README.md
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = True
camera.vflip = True
camera.crop = (0.0, 0.0, 1.0, 1.0)

# test image so we know its working
print "Capturing test image in 3 seconds"
sleep(1)
camera.capture('/home/pi/Desktop/capture/testimage.jpg')

# Create daily directories (automatically doesnt create if it exists)
create_fecha_dir = "mkdir /home/pi/Desktop/capture/"+fecha_old
os.system(create_fecha_dir)

# Setup up PIR
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

# capture images
while 1:
    if GPIO.input(PIR_PIN):
        print "Motion Detected!"
        for num in range(1,2):
            print(num)

            # update variables
            #stdout.write(".")
            #stdout.flush()
            current_time = time.time()
            elapsed_time = math.ceil(current_time-start_time)
            hour = datetime.now().strftime("%H")
            #print(hour)
            tiempo = datetime.now().strftime("%H-%M-%S")
            fecha = datetime.now().strftime("%Y-%m-%d")
            fecha_tiempo = fecha+"_"+tiempo

            # new hour (BEFORE NEW DAY; send files before a new dir is made for a new day)
            if hour!=hour_old:
                # send dropbox files
                hour_old = hour
                print("new hour. send dropbox files")

            # new day
            if fecha!=fecha_old:
                create_fecha_dir = "mkdir /home/pi/Desktop/capture/"+fecha
                os.system(create_fecha_dir)
                fecha_old = fecha
                print("New day. created new directory")
    
            # create new directories
            fecha_dir = "/home/pi/Desktop/capture/"+fecha
            create_fecha_dir = "mkdir /home/pi/Desktop/capture/"+fecha
            jpg_name = fecha_tiempo+".jpg"
            jpg_name_usb = fecha_tiempo+"_usb"+".jpg"
            jpg_dir = fecha_dir+"/"+jpg_name
            jpg_dir_usb = fecha_dir+"/"+jpg_name_usb
            jpg_dir_dropbox = "/"+dropbox_name+"/"+fecha+"/"+jpg_name

            # capture image (pi)
            camera.capture(jpg_dir)

            # capture image (usb)
            capture_cmd_usb = "fswebcam -r 1280x720 --fps 15 -S 10 --quiet "+jpg_dir_usb
            os.system(capture_cmd_usb)

            # send image
            # https://www.andreafabrizi.it/2016/01/01/Dropbox-Uploader/
            if dropbox==1:

                # get IP address
                proc = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE)
                (out,err) = proc.communicate()
                ip = out[0:12]
                ip = ""
                jpg_name_with_ip = fecha_tiempo+".jpg"
                jpg_name_with_ip_usb = fecha_tiempo+"_usb.jpg"
                jpg_dir_with_ip = fecha_dir+"/"+jpg_name_with_ip
                jpg_dir_with_ip_usb = fecha_dir+"/"+jpg_name_with_ip_usb
                jpg_dir_dropbox_with_ip = "/"+dropbox_name+"/picam/"+fecha+"/"+jpg_name_with_ip
                jpg_dir_dropbox_with_ip_usb = "/"+dropbox_name+"/usbcam/"+fecha+"/"+jpg_name_with_ip_usb
                send_cmd = "/home/pi/dropbox_uploader.sh upload "+jpg_dir+" "+jpg_dir_dropbox_with_ip
                os.system(send_cmd)
                send_cmd_usb = "/home/pi/dropbox_uploader.sh upload "+jpg_dir_usb+" "+jpg_dir_dropbox_with_ip_usb
                os.system(send_cmd_usb)

                # delete image
                os.system("rm "+jpg_dir)
                os.system("rm "+jpg_dir_usb)

                # change name for status
                jpg_name = jpg_name+" sent through dropbox"

            # terminal status
            print(jpg_name)
        sleep(3)
    sleep(1)
        
