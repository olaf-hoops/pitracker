import time
import math
import sys
from pygsm import GsmModem

# Switch GPS on
def SwitchGPSon():
    print "Switching GPS on ..."
    reply = gsm.command('AT+CGNSPWR=1')
    print reply
    print

def SwitchGPSoff():
    print "Switching GPS off ..."
    reply = gsm.command('AT+CGNSPWR=0')
    print reply
    print
    
def SendGPSPosition():
    print "Getting GPS position ..."
    reply = gsm.command('AT+CGNSINF')
    list = reply[0].split(",")
    UTC = list[2][8:10]+':'+list[2][10:12]+':'+list[2][12:14]
    Latitude = list[3]
    Longitude = list[4]
    Altitude = list[5]
    print 'Position: ' + UTC + ', ' + Latitude + ', ' + Longitude + ', ' + Altitude
    # Text to mobile
    Message = ' Position: ' + UTC + ', ' + str(Latitude) + ', ' + str(Longitude) + ', ' + str(Altitude) + ' http://maps.google.com/?q=' + str(Latitude) + ',' + str(Longitude)
    print "Sending to mobile " + MobileNumber + ": " + Message
    gsm.send_sms(MobileNumber, Message)


# Set mobile number here
MobileNumber = "01752051617"
lastmessage = 'Stop'

print "Booting modem ..."
gsm = GsmModem(port="/dev/serial0")
gsm.boot()

print "Modem details:"
reply = gsm.hardware()
print "Manufacturer = " + reply['manufacturer']
print "Model = " + reply['model']

# Try and get phone number
reply = gsm.command('AT+CNUM')
if len(reply) > 1:
	list = reply[0].split(",")
	phone = list[1].strip('\"')
	print "Phone number = " + phone
print
	
print "Deleting old messages ..."
gsm.query("AT+CMGD=70,4")
print

SwitchGPSon()

print "Boot successful, waiting for messages ..."

while True:
        
    # Check messages
	message = gsm.next_message()
	
	if message:
		print "loop 1"
		print message
		text = message.text
		if text[0:5] == 'Start':
			print "Start sending Position ..."
			SendGPSPosition()
			lastmessage = 'Start'
			time.sleep(300)
       		elif text[0:4] == 'Stop':
			print "Text was Stop. Stop sending"
			lastmessage = 'Stop'
	else:
		if lastmessage == 'Start':
			print(lastmessage+' loop2')
			SendGPSPosition()
			time.sleep(300)
		else:
			time.sleep(10)
