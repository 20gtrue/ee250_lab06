import grovepi
import time

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

#Connect the Grove LCD RGB Backlight
#This device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# Set initial threshold distance to 20cm
threshold_distance = 20

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

grovepi.pinMode(potentiometer,"INPUT")

def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)
    
    
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))
        
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))


while True:
    try:
        # Read sensor value from potentiometer
        sensor_value = grovepi.analogRead(potentiometer)

        # Calculate voltage
        voltage = round((float)(sensor_value) * adc_ref / 1023, 2)

        # Calculate rotation in degrees (0 to 300)
        degrees = round((voltage * full_angle) / grove_vcc, 2)

        # Map the degrees to a threshold distance between 5cm to 100cm
        threshold_distance = int(degrees / full_angle * 95 + 5)

        # Read distance value from Ultrasonic
        distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        # Check if the object is within the threshold distance
        if distance < threshold_distance:
            text = "OBJ PRES"
            r, g, b = 255, 0, 0
        else:
            text = "          "
            r, g, b = 0, 255, 0

        # Set the backlight color of the LCD based on the threshold status
        grovepi.setRGB(r, g, b)

        # Display the threshold distance on the top line of the LCD
        top_line_text = "Threshold: {}cm".format(threshold_distance)
        setText(top_line_text)

        # Display the current distance on the bottom line of the LCD
        bottom_line_text = "Distance: {}cm".format(distance)
        setText_norefresh(bottom_line_text)
        
      	# Set the backlight color of the LCD based on the threshold status
        grovepi.setRGB(r, g, b)

        # Display the threshold distance on the top line of the LCD
        top_line_text = "Threshold: {}cm".format(threshold_distance)
        setText(top_line_text)

        # Display the current distance on the bottom line of the LCD
        bottom_line_text = "Distance: {}cm".format(distance)
        setText_norefresh(bottom_line_text)
    
    except Exception as e:
    	print ("Error:{}".format(e))

    time.sleep(0.1) # don't overload the i2c bus
