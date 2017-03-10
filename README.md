# TDCamera
Raspberry Pi Python Security Camera with both picam and USB camera, and PIR motion detection

## myscript.py
Main python script to run. Some capabilities include
- use dateutil to get current time in your time zone, regardless of where you apply this script.
- takes a test picture to adjust the camera locations
- ability to control picamera values (sharpness, contrast, ISO, flips, etc.)
- using dropbox_uploader.sh to push pictures to dedicated folder, with new folder/directory automatically created daily.
- uses a PIR sensor to detect motion and capture images
- appends IP address to images taken and sends through dropbox_uploader.sh

## usb.py
Python script that gets the IP address of the raspberry pi, and saves a blank image with the IP as the title.
I couldn't get a static IP address, so this is a hack to get the raspberry pi IP address so I can ssh into it later.

## run.sh
Bash script to run usb.py on start-up of pi. 
