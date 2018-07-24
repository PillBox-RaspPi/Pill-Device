import RPi.GPIO as GPIO
import pigpio
import time
import datetime
import smtplib
GPIO.setmode(GPIO.BCM)
pi=pigpio.pi()

debug = True

#sets the alarm time
ALARM =  '0830'
ALARMEND = '0840'

#Setting up the pins on the right of the breakout board for OUTPUT: LEDs
for i in [14, 15, 23, 24, 25, 8, 7]:
     pi.set_mode(i, pigpio.OUTPUT)

#Setting up the pins on the left of the breakout board for INPUT: hall effect sensors
sensor_pins = [2, 3, 4, 17, 27, 22, 10]
for i in sensor_pins:
    pi.set_mode(i,pigpio.INPUT)
    pi.set_pull_up_down(i, pigpio.PUD_UP)

LED_pins = {6: 18, 0: 23, 1: 24, 2: 25, 3: 12, 4: 16, 5: 20}

Sunday = {'LED_pin':14, 'sensor_pin': 2, 'day_num': 6, 'boxname': 'Sunday'}
Monday = {'LED_pin': 25, 'sensor_pin': 3, 'day_num': 0, 'boxname': 'Monday'}
Tuesday = {'LED_pin': 23, 'sensor_pin': 4, 'day_num': 1, 'boxname': 'Tuesday'}
Wednesday = {'LED_pin': 24, 'sensor_pin': 17, 'day_num': 2, 'boxname': 'Wednesday'}
Thursday = {'LED_pin': 25, 'sensor_pin': 27, 'day_num': 3, 'boxname': 'Thursday'}
Friday = {'LED_pin': 8, 'sensor_pin': 22, 'day_num': 4, 'boxname': 'Friday'}
Saturday = {'LED_pin': 7, 'sensor_pin': 10, 'day_num': 5, 'boxname': 'Saturday'}

boxes = [Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday]



#returns the current time
def timenow():
    return time.strftime('%H%M')

sentmails = {sentmail1, sentmail3, sentmail4}

timestamp = datetime.date.today()

if resetday != today:
    for i in sentmails:
         i = False
    sentmail2 = [False]*7
    sentmail5 = [False]*7
    timestamp = datetime.date.today()

#defines the email function
def sendemail(from_addr = 'pillbox.rasppi@gmail.com',
                to_addr_list = ['elizabeth@yallop.org'],
                cc_addr_list = ['elizabeth@yallop.org'], 
                login = 'pillbox.rasppi@gmail.com', 
                password = 'eyrasppi',
                smtpserver = 'smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


#defines the LED flashing function
def flashLED(LED_pin, bleep = False):
    pi.write(LED_pin, True)
    time.sleep(1)
    pi.write(LED_pin, False)
    time.sleep(1)

#defines the sensor-checking function
def checkbox(box):

        if pi.read(box['sensor_pin']) == 0 and sentmail1 != True:
            sendemail( subject      = 'Test email',
                message      = 'At' + time.strftime('%H%M') + ', ' + box['boxname'] + 's box was opened.')
            sentmail1 = True
        while pi.read(box['sensor_pin']) == 0:
            flashLED(box['LED_pin'])


print('Setup Complete!')

while True:
    #Checks if today is Sunday; if so, reminds user to refill box 10 minutes before med time.
    if datetime.datetime.now().weekday() == 6 and timenow() == ('0820'):
        for LED_pin in LED_pins:
            flashLED(LED_pin)


    #Checks that no pills are taken before med time
    if debug:
        print('timenow = ', timenow(), ' ALARM = ', ALARM)
    while timenow() < ALARM:
        print('time before ALARM')
        for box in boxes:
            checkbox(box)


    #At ALARM time, flashes correct light, checks which box is opened and texts carer correctly
    while timenow() >= ALARM and timenow() < ALARMEND:
        flashLED(box['LED_pin'])
        for box in boxes:
            if (day_num != today) and pi.read(box['sensor_pin']) == 0 and not sentmail2[day_num]:
                sendemail(subject      = 'Alert!',
                    message      = 'The wrong box was opened at med time! Maybe check up on the user?')
                    sentmail2[day_num] = True
            elif (day_num == today) and pi.read(box['sensor_pin']) == 0 and not sentmail3:
                sendemail(subject      = 'Check-in',
                    message      = 'The correct box was opened at the correct time today.',)
                    sentmail3 = True
                pilltaken = True

    #alerts the carer if the pills weren't taken
    if timenow() == ALARMEND and (pilltaken != True) and sentmail4 != True:
        sendemail(subject      = 'Alert!',
                    message      = 'The pills werent taken at med time today. Maybe check up on the user?')
        sentmail4 = True


    #checks that the pills aren't taken after med time
    while timenow() > ALARMEND:
        for box in boxes:
            checkbox(box)
            if pi.read(box['sensor_pin']) == 0 and sentmail5[day_num] != True:
                sendemail(subject      = 'Alert!',
                    message      = 'Its more than 10 minutes past med time, but ' + box['boxname'] + 's box was opened.')
                sentmail5[day_num] = True

    if timenow() == ('0845') and logged != True:
        timelog += 1
        logged = True
