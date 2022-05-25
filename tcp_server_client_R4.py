import socket
import threading
import time
import l298n_R4 as l298n
import drivers
global s
import RPi.GPIO as GPIO
try:
    display = drivers.Lcd()
except:
    print("Failed to init display")

receiver_size = 50000
thread_details = []
thread_count = 0
GPIO.setmode(GPIO.BOARD)
mq3 = 19
GPIO.setup(mq3, GPIO.IN)
motor_speed = 0
engine_start = False
motor_direction = ""

def create_socket(port:int):
    s = socket.socket()
    ipaddr = ""
    s.bind((ipaddr, port))
    print(f"SERVER IP: {socket.gethostbyname(socket.gethostname())}\nSERVER PORT : {port}")
    s.listen(5)
    try:
        display.lcd_display_string(f"client connected{socket.gethostbyname(socket.gethostname())}", 1)
    except:
        print("failed to print in LCD")

    return s


def handel_client(conn, ip, thread_count, s):
    connected = True
    while connected == True:
        new_message = True
        while new_message == True:
            try:
                rec = conn.recv(5000).decode("utf-8")
                start_header = "<----start_header---->"
                end_header = "<----end_header---->"
                start_message = "<----start_message---->"
                end_message = "<----end_message---->"
                start_message_length = "<----start_message_length---->"
                end_message_length = "<----end_message_length---->"
                message_size = 10
                number_of_start_header = rec.count(start_header)
                number_of_end_header = rec.count(end_header)
                number_of_commands = number_of_end_header
                split_data = rec.split(end_header)
                for i in range(len(split_data)):
                    if (start_message in split_data[i]) and (end_message in split_data[i]):
                        command = split_data[i].replace(start_header, "")
                        command = command.replace(end_header, "")
                        command = command.replace(start_message, "")
                        command = command.replace(end_message, "")
                        command = command.replace(start_message_length,"")
                        command = command.replace(end_message_length,"")
                        # print(command)
                        if "disconnect_matrix_led" in command:
                            s.shutdown(socket.SHUT_RDWR)
                            s.close()
                        if "l298n" in command:
                            # print("entered l298n")
                            command = command.replace("l298n","")
                            l298_data = command.split(",")
                            motor_direction = l298_data[0]
                            motor_speed = l298_data[1]
                            try:
                                display.lcd_clear()
                            except:
                                print("failed to print in LCD")
                            if motor_direction != "forward":
                                l298n.handler(motor_direction, motor_speed)

                        elif "mq3" in command:
                            command = command.replace("mq3", "")
                            if "start engine" in command:
                                if GPIO.input(mq3) == 1:
                                    engine_start = True
                                    for i in range(len(thread_details)):
                                        result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,
                                                      "mq3 alcohol not detected")
                                    try:
                                        display.lcd_clear()
                                        display.lcd_display_string("ENGINE STARTED", 1)
                                    except:
                                        print("failed to print in LCD")
                                elif GPIO.input(mq3) == 0:
                                    engine_start = False
                                    for i in range(len(thread_details)):
                                        result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,
                                                      "mq3 alcohol detected")
                                    try:
                                        display.lcd_clear()
                                        display.lcd_display_string("alcohol detected", 1)
                                    except:
                                        print("failed to print in LCD")

                            elif "stop engine" in command:
                                engine_start = False
                                l298n.handler("forward",0)
                                try:
                                    display.lcd_clear()
                                    display.lcd_display_string("ENGINE STOP", 1)
                                except:
                                    print("failed to print in LCD")
                                for i in range(len(thread_details)):
                                    result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,
                                                  "engine stoped")
                        elif "zone_alert" in command:
                            command = command.replace("zone_alert", "")
                            if ("hospital" in command):
                                # print(f"length of thread details :${len(thread_details)}")
                                # print(thread_details)
                                disconnected_client = []
                                if "hospital" in command:
                                    try:
                                        display.lcd_clear()
                                        display.lcd_display_string("hospital zone", 1)
                                        display.lcd_display_string("do not exceed 40", 2)
                                    except:
                                        print("failed to print in LCD")
                                    for i in range(len(thread_details)):
                                        result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,"hospital zone")

                            elif "normal" in command:
                                try:
                                    display.lcd_clear()
                                    display.lcd_display_string("normal zone", 1)
                                    display.lcd_display_string("do not exceed 40", 2)
                                except:
                                    print("failed to print in LCD")
                                for i in range(len(thread_details)):
                                    result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,
                                                  "normal zone")
                            elif "school" in command:
                                try:
                                    display.lcd_clear()
                                    display.lcd_display_string("school zone", 1)
                                except:
                                    print("failed to print in LCD")
                                for i in range(len(thread_details)):
                                    result = send(thread_details[i]['conn'], thread_details[i]['ipaddress'], s,
                                                  "hospital zone")
                        if "matrix_led" in command:
                            command = command.replace(start_message_length, "")
                            command = command.replace("<----matrix_led---->", "")
                            message_size = command.split(end_message_length)
                            message = message_size[1]
                            data = message
                            data = data.replace("[", "")
                            data = data.replace("]", "")
                            data = data.split(",")
                            ret_data = []
                            data1 = []
                            for i in range(len(data)):
                                if i % 5 != 0 or i == 0:
                                    data1.append(data[i])
                                    if i == 174:
                                        ret_data.append(data1)
                                        data1 = []
                                else:
                                    ret_data.append(data1)
                                    data1 = []
                                    data1.append(data[i])
                            rec = []
                    else:
                        continue
            except:
                break



def display_data(data):
    def display_internal_data(data):
        print(data)
    t = threading.Thread(target=display_internal_data,args=(data,))
    t.start()


def accept_connection(s,thread_count):
    while True:
        try:
            conn, ip = s.accept()
            thread_count += 1
            s.setblocking(1)
            print(str(ip[0]))
            thread_name = str(ip[0]) + ":" + str(thread_count)
            print(thread_name)
            thread = threading.Thread(target=handel_client, args=(conn, ip, thread_count, s), name=thread_name)
            thread.start()
            thread_data = {
                "ipaddress": ip[0],
                "name": thread_name,
                "thread_number": thread_count,
                "conn": conn,
                "start_time": time.time()
            }
            thread_details.append(thread_data)
            print(thread_details)
            print(threading.active_count() - 1)
            print("send message thread started")
            time.sleep(0.02)

        except:
            print("suresh")
            break



def send(conn, ip, s, data):
    print("thread 2 start")
    i = 0
    try:
        conn.send(str.encode(f"{data}\n"))
        time.sleep(0.2)
        return 'success'
    except:
        print(f"{ip}: DISCONNECTED")
        return "disconnected"
        # for i in len(thread_details):
        #     if (ip in thread_details):
        #         thread_details.pop(i)






if __name__ == '__main__':
    port = int(input("ENTER PORT NUMBER : "))
    s = create_socket(port)
    accept_connection = threading.Thread(target=accept_connection(s,thread_count))
    accept_connection.start()
    print("accept_connection thread started")
    print("send_message thread started")

