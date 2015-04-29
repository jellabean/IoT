# 4Paw_Fire
#
# This program is part of the Intel IoT Incubator "Round 2" project that was one of twenty selected for funding/implementation.
#
# Standard GNU sharing/non commercial/rights/acknowledgement stuff applies.
#

# Import Libraries
import mraa
import time
import pyupm_grove as upm
import pyupm_yg1006 as flame_sensor
import pyupm_buzzer as upmBuzzer
import pyupm_waterlevel as upmWaterlevel

# Global Definitions
On=1
Off=0
Read=0
Write=1
Water=Off
#
temp_alert=100
hum_alert=10
temp_warn=80
hum_warn=20 

# Sensor Addresses
button_1_addr=2
button_2_addr=3
flame_addr=4 
h2o_level_addr=5
relay_addr=7
buzzer_addr=6
LED_onboard_addr=13
#
temp_hum_addr=0
smoke_addr=1 
h2o_flow=2

# Sensor Bounds
button_range=[0,1]
flame_range=[0,1]
LED_range=[0,1]
relay_range=[0,1]
buzzer_range=[0,1]

# Sensor definition
button_1 = upm.GroveButton(button_1_addr)
button_2 = upm.GroveButton(button_2_addr)
relay = upm.GroveRelay(relay_addr)
flame = flame_sensor.YG1006(flame_addr)
buzzer = upmBuzzer.Buzzer(buzzer_addr) 
h2o_level=upmWaterlevel.WaterLevel(h2o_level_addr)

# Function Definition

#
def test_relay():
	"This function will test the relay"
	for i in range (0,3):
	    relay.on()
    	    time.sleep(1)
    	    relay.off()
    	    time.sleep(1)

#
def test_con ():
	"This function will test the installed sensors, etc"
	print ("Run test functions")
	test_relay()
	while 1:
		print ("Water level is ",h2o_level.isSubmerged())
    	    	time.sleep(1)
#
def config ():
	"This function will config sensors levels, alert notifications, etc"
	print ("Run config functions")
#
def activate(Water):
	"This function will change the water condition"
	print ("If Water == On : get h2o_flow; while h2o_flow > Off : if relay.isOn() : relay(Off); time.sleep(2); get h2o_flow; Water=Off")
	print ("elif : get h2o_flow; while h2o_flow < On : if relay.isOff() : relay(On); time.sleep(2); get h2o_flow; Water=On")
	return(Water);
#
def alert ():
	"This function will send an alert"
	count=3
	for i in range(count): 
		buzzer.playSound(500,100000)
		buzzer.playSound(0,1)
		time.sleep(1)
	buzzer.playSound(0,0)
#
def run ():
	"This function will query sensors and take action"
	print ("Get sensor data (flame, smoke, temp, hum, h2o_sensor, h2o_flow)")
	button_val=0
	while button_val == 0 :
		flame_val=flame.flameDetected()
		if flame_val : # and Water == Off :
			print ("Flame is:",flame_val)
			alert()
			activate(Water)
		print ("Flame is:",flame_val)
		button_val=button_1.value()
		time.sleep(2)
	print ("If h2o_sensor : alert and shut down") # Water has intruded into system enclosure!!
	print ("If (flame or smoke) and Water == Off : alert and activate(Water)") # Detected Flame or Smoke--there is a FIRE!!
	print ("If temp > temp_alert and hum < hum_alert and Water == Off : send alert, activate(Water) ") # Conditions indicate a fire eminent 
	print ("elif temp > temp_warn and hum < hum_warn : send alert ") # Conditions approaching fire condition
	print ("elif Water == On : alert and activate(Water)") # Fire conditions no longer exist. 
	

#

# Main
ask=""
while ask != "Q":
	ask = raw_input ("(T)est, (C)onfig, (R)un, (Q)uit:")
	ask = ask.upper()
	if ask == "T" : test_con()
	elif ask == "C" : config()
	elif ask == "R" : run()
	elif ask == "Q" : print ("Exiting program")
	
