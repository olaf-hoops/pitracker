import time
import math
import sys
from pygsm import GsmModem

# Set mobile number here
MobileNumber = "01752051617"

print "Booting modem ..."
gsm = GsmModem(port="/decdserial0")
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
	
# Switch GPS on
print "Switching GPS on ..."
reply = gsm.command('AT+CGNSPWR=1')
print reply
print

print "Boot successful, waiting for messages ..."
while True:
    
    # Get position
	reply = gsm.command('AT+CGNSINF')
	list = reply[0].split(",")
	if len(list[2]) > 14:
		UTC = list[2][8:10]+':'+list[2][10:12]+':'+list[2][12:14]
		Latitude = list[3]
		Longitude = list[4]
		Altitude = list[5]
		print 'Position: ' + UTC + ', ' + Latitude + ', ' + Longitude + ', ' + Altitude
    
    # Check messages
	message = gsm.next_message()
	if message:
		print message
		text = message.text
		if text[0:2] == 'Go':
			print "Text was Go. Doing Stuff now"
            
			# Text to my mobile
			Message = PayloadID + ' position: ' + UTC + ', ' + str(Latitude) + ', ' + str(Longitude) + ', ' + str(int(Altitude)) + ' http://maps.google.com/?q=' + str(Latitude) + ',' + str(Longitude)
			print "Sending to mobile " + MobileNumber + ": " + Message
			# gsm.send_sms(MobileNumber, Message)
	else:
		time.sleep(1)