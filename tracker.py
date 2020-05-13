import time
import math
import sys
from pygsm import GsmModem


print "Booting modem ..."
gsm = GsmModem(port="/dev/ttyserial0")
gsm.boot()

print "Modem details ..."
reply = gsm.hardware()
print "Manufacturer = " + reply['manufacturer']
print "Model = " + reply['model']

# Try and get phone number
reply = gsm.command('AT+CNUM')
if len(reply) > 1:
	list = reply[0].split(",")
	phone = list[1].strip('\"')
	print "Phone number = " + phone
	
print "Waiting for messages ..."
while True:
	message = gsm.next_message()
	if message:
		print message
		text = message.text
		if text[0:2] == 'Go':
			print "Text was Go. Doing Stuff now"
			
	else:
		time.sleep(1)