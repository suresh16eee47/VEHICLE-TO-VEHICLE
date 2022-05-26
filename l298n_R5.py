import threading
import time
import RPi.GPIO as GPIO
import hcsr04_R5 as hscr04
import drivers
display = drivers.Lcd()
GPIO.setwarnings(False)
motor_1_enable = 33
motor_1_A = 35
motor_1_B = 37
motor_2_enable = 36
motor_2_A = 38
motor_2_B = 40
direction_1 = ""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_1_enable, GPIO.OUT)
GPIO.setup(motor_1_A, GPIO.OUT)
GPIO.setup(motor_1_B, GPIO.OUT)
GPIO.setup(motor_2_enable, GPIO.OUT)
GPIO.setup(motor_2_A, GPIO.OUT)
GPIO.setup(motor_2_B, GPIO.OUT)
motor_1_speed = GPIO.PWM(motor_1_enable, 1000)
motor_2_speed = GPIO.PWM(motor_2_enable, 1000)
motor_1_speed.start(0)
motor_2_speed.start(0)


def forward(speed):
    speed_1 = int(speed)
    GPIO.output(motor_1_A, GPIO.HIGH)
    GPIO.output(motor_1_B, GPIO.LOW)
    GPIO.output(motor_2_A, GPIO.HIGH)
    GPIO.output(motor_2_B, GPIO.LOW)
    display.lcd_clear()
    display.lcd_display_string(f"<--FORWARD-->", 1)
    display.lcd_display_string(f"Motor speed{speed_1}" , 2)
    motor_1_speed.ChangeDutyCycle(speed_1)
    motor_2_speed.ChangeDutyCycle(speed_1)



def reverse(speed):
    speed_1 = int(speed)
    GPIO.output(motor_1_A, GPIO.LOW)
    GPIO.output(motor_1_B, GPIO.HIGH)
    GPIO.output(motor_2_A, GPIO.LOW)
    GPIO.output(motor_2_B, GPIO.HIGH)
    display.lcd_clear()
    display.lcd_display_string(f"<--REVERSE-->", 1)
    display.lcd_display_string(f"Motor speed{speed_1}", 2)
    motor_2_speed.ChangeDutyCycle(speed_1)
    motor_1_speed.ChangeDutyCycle(speed_1)

def right(speed):
    speed_1 = int(speed)
    # print(f"right configured with speed : ${speed}")
    GPIO.output(motor_1_A, GPIO.LOW)
    GPIO.output(motor_1_B, GPIO.HIGH)
    GPIO.output(motor_2_A, GPIO.HIGH)
    GPIO.output(motor_2_B, GPIO.LOW)
    display.lcd_clear()
    display.lcd_display_string(f"<--RIGHT-->", 1)
    display.lcd_display_string(f"Motor speed{speed_1}", 2)
    motor_1_speed.ChangeDutyCycle(speed_1)
    motor_2_speed.ChangeDutyCycle(speed_1)


def left(speed):
    speed_1 = int(speed)
    # print(f"left configured with speed : ${speed}")
    GPIO.output(motor_1_A, GPIO.HIGH)
    GPIO.output(motor_1_B, GPIO.LOW)
    GPIO.output(motor_2_A, GPIO.LOW)
    GPIO.output(motor_2_B, GPIO.HIGH)
    display.lcd_clear()
    display.lcd_display_string(f"<--LEFT-->", 1)
    display.lcd_display_string(f"Motor speed{speed_1}", 2)
    motor_1_speed.ChangeDutyCycle(speed_1)
    motor_2_speed.ChangeDutyCycle(speed_1)

def handler(direction,speed):
    if direction == "forward":
        direction_1 = "forward"
        forward(int(speed))
    elif direction == "reverse":
        reverse(int(speed))
    elif direction == "left":
        left(int(speed))
    elif direction == "right":
        right(int(speed))
