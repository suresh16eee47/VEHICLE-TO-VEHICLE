# Libraries
import threading
import RPi.GPIO as GPIO
import time
import tcp_server_client_R4 as tcp_server_client
import l298n_R4 as l298n
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
distance_g = 0

def distance():
    global distance_g
    motor_direction = tcp_server_client.motor_direction
    engine_start = tcp_server_client.engine_start
    while True:
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        distance_g = distance
        time.sleep(0.002)
        if tcp_server_client.engine_start == True:
            if (tcp_server_client.motor_direction == "forward" and distance_g <= 5 and tcp_server_client.motor_speed >= 21):
                l298n.forward(20)
            elif (tcp_server_client.motor_direction == "forward" and distance_g <= 5 and tcp_server_client.motor_speed <= 20):
                l298n.forward(tcp_server_client.motor_speed)
            elif (tcp_server_client.motor_direction == "forward" and distance_g <= 10 and tcp_server_client.motor_speed >= 36):
                l298n.forward(35)
            elif (tcp_server_client.motor_direction == "forward" and distance_g <= 10 and tcp_server_client.motor_speed <= 35):
                l298n.forward(tcp_server_client.motor_speed)
            elif (tcp_server_client.motor_direction == "forward" and distance_g <= 15 and tcp_server_client.motor_speed >= 51):
                l298n.forward(50)
            elif (tcp_server_client.motor_direction == "forward" and distance_g <= 15 and tcp_server_client.motor_speed <= 50):
                l298n.forward(tcp_server_client.motor_speed)



threading.Thread(target=distance,args=()).start()





