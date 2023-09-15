import RPi.GPIO as IO  #calling for header file which helps in using GPIO’s of PI
import time            #we are calling for time to provide delays in program
import datetime        #we are calling for DATE
import SDL_DS1307      #calling for special functions which helps us interface RTC module
h=0                    #integers for storing values
m=0
alarm=0
string_of_characters = 0

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)  #entering I2c address, which we recorded previously
ds1307.write_now()

IO.setwarnings(False)  #do not show any warnings
IO.setmode (IO.BCM)    #programming the GPIO by BCM pin numbers. (like PIN29 as'GPIO5')

#initialize GPIO17,27,24,23,18,26,5,6,13,19 as an output
IO.setup(17,IO.OUT)
IO.setup(27,IO.OUT)
IO.setup(24,IO.OUT)
IO.setup(23,IO.OUT)
IO.setup(18,IO.OUT)
IO.setup(26,IO.OUT)
IO.setup(5,IO.OUT)
IO.setup(6,IO.OUT)
IO.setup(13,IO.OUT)
IO.setup(19,IO.OUT)

IO.setup(21,IO.IN)  #initialize GPIO21 as an input.
IO.setup(20,IO.IN)  #initialize GPIO20 as an input.
IO.setup(16,IO.IN) 
IO.setup(12,IO.IN) 
IO.setup(25,IO.IN) 

IO.setup(22,IO.OUT) #initialize GPIO22 as an output.

def send_a_command (command):  #steps for sending a command to 16*2LCD
    pin=command
    PORT(pin);
    IO.output(17,0)
    IO.output(27,1)
    time.sleep(0.001)
    IO.output(27,0)
    pin=0
    PORT(pin); 

def send_a_character (character):#steps for sending a character to 16*2 LCD
    pin=character
    PORT(pin);
    IO.output(17,1)
    IO.output(27,1)
    time.sleep(0.001)
    IO.output(27,0)
    pin=0
    PORT(pin);

def PORT(pin):            #assigning level for PI GPIO for sending data to LCD through D0-D7
    if(pin&0x01 == 0x01):
        IO.output(24,1)
    else:
        IO.output(24,0)
    if(pin&0x02 == 0x02):
        IO.output(23,1)
    else:
        IO.output(23,0)
    if(pin&0x04 == 0x04):
        IO.output(18,1)
    else:
        IO.output(18,0)
    if(pin&0x08 == 0x08):
        IO.output(26,1)
    else:
        IO.output(26,0)    
    if(pin&0x10 == 0x10):
        IO.output(5,1)
    else:
        IO.output(5,0)
    if(pin&0x20 == 0x20):
        IO.output(6,1)
    else:
        IO.output(6,0)
    if(pin&0x40 == 0x40):
        IO.output(13,1)
    else:
        IO.output(13,0)
    if(pin&0x80 == 0x80):
        IO.output(19,1)
    else:
        IO.output(19,0)

def send_a_string(string_of_characters):  #steps for sending string of characters to LCD
  string_of_characters = string_of_characters.ljust(16," ")
  for i in range(16):
    send_a_character(ord(string_of_characters[i])) 
#send characters one by one until all the strings characters are sent through data port

while 1: 
    send_a_command(0x38); #use two lines of LCD
    send_a_command(0x0E); #screen and cursor ON
    send_a_command(0x01); #clear screen
    time.sleep(0.1)       #sleep for 100msec
    while 1:
        if (IO.input(21) == 0):
            if (h<23):    #if button1 is pressed and hour count is less than 23 increment 'h' by one
                h=h+1

        if (IO.input(20) == 0):
            if (h>0):     #if button2 is pressed and hour count is more than 0 decrease 'h' by one
                h=h-1

        if (IO.input(16) == 0):
            if (m<59):    #if button3 is pressed and minute count is less than 59 increment 'm' by one
                m=m+1

        if (IO.input(12) == 0):
            if (m>0):     #if button4is pressed and minute count is more than 0 decrease 'm' by one
                m=m-1

        if (IO.input(25) == 0):  #if button5 is pressed toggle Alarm ON and OFF
            if (alarm==0):
                alarm=1
            else:
                alarm=0
            time.sleep(0.1)

        if (alarm==1):
            send_a_command(0x80 + 0x40 + 12);
            send_a_string("ON");  #if alarm is set, then display "ON" at the 12th position of second line of LCD

            if ((h==ds1307._read_hours())):
                if ((m==ds1307._read_minutes())):
                    IO.output(22,1)  #if alarm is set, and hour-minute settings match the RTC time, trigger the buzzer

        if (alarm==0):
            send_a_command(0x80 + 0x40 + 12);
            send_a_string("OFF"); #if alarm is OFF, then display "OFF" at the 12th position of second line of LCD
            IO.output(22,0)       #turn off the buzzer         

        send_a_command(0x80 + 0);   #move courser to 0 position
        send_a_string ("Time:%s:%s:%s" % (ds1307._read_hours(),ds1307._read_minutes(),ds1307._read_seconds()));
        #display RTC hours, minutes, seconds
        send_a_command(0x80 + 0x40 + 0);  #move courser to second line
        send_a_string ("Alarm:%s:%s" % (h,m));  #show alarm time
        time.sleep(0.1)  #wait for 100msec