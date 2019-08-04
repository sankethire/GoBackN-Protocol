import socket
import time
import random
import sys

open('sender_log.txt', 'a+w').close()
f = open("sender_log.txt", 'r+b')
# defaults: error_prob = 0.1; window_size = 7; prop_delay = -1
# prop_delay=-1 will introduce delay in ms. This may lead to errors.
error_prob = 0.1
window_size = 7
prop_delay = 0.1

def create_packet():
    payload = ""
    # char = 1 byte = 8 bits
    # 512 bits = 64 bytes  &&  2024 bits = 253 bytes
    payload_size = random.randint(64,253)
    for i in range(payload_size):
        small_or_large = random.randint(0,1)
        if(small_or_large == 0):
            c = random.randint(97,122)
            payload += chr(c)
        else:
            c = random.randint(65,90)
            payload += chr(c)
    return payload

def append_packet():
    global window_size
    global buffer

    while(len(buffer) < window_size):
        buffer.append(create_packet())

def delete_packet(x):
    global buffer
    pos = x-1

    while(pos >= 0):
        del buffer[pos]
        pos -=1

def time_delay(delay):
	if(delay == -1):
		sleep_time = random.randint(0,5)*0.001
		time.sleep(sleep_time)
	else:
		time.sleep(delay)

# print(create_packet())
buffer = []

sock = socket.socket()
host = socket.gethostname()
port = 8009
sock.bind((host , port))
sock.listen(0)
connection , addr = sock.accept()

# ACK size = 256/8 bytes = 32 bytes
connection.send("Sender is Connected!")
reciever_test = connection.recv(44)
print(reciever_test)

packets_this_second = 0
pack = 1
# ack_no = 1
abhi_time = int(time.time())
window = 1
error_pos = 0
pack_error_pos = 0
error_till_now = False

while(True):
    if((time.time() - abhi_time) > 1):
        abhi_time = int(time.time())
        packets_this_second = 0
    else:
        if(packets_this_second <= 400):

            append_packet()

            while(window <= window_size):

                time_delay(prop_delay)

                error_new = random.randint(1,10)
                if(error_new == 1):
                    print("SENDER: Sending Packet " + str(pack) + " (error)")
                    f.write("SENDER: Sending Packet " + str(pack) + " (error) \n")
                    connection.send("**32*BYTES*HEADER*HAS*ERRORS*1**" + buffer[window-1])
                else:
                    print("SENDER: Sending Packet " + str(pack))
                    f.write("SENDER: Sending Packet " + str(pack) + "\n")
                    connection.send("**32*BYTES*HEADER*HAS*ERRORS*0**" + buffer[window-1])

                if(error_till_now == False):
                    ack = connection.recv(32)
                    # print("ack: " + ack)
                    if(ack == "***32*BYTES*ACKN*HAS*ERRORS*1***"):
                        print("SENDER: Recieved Ack " + str(pack) + " (error)")
                        f.write("SENDER: Recieved Ack " + str(pack) + " (error) \n")
                        error_till_now = True
                        error_pos = window
                        pack_error_pos = pack
                    else:
                        print("SENDER: Recieved Ack " + str(pack))
                        f.write("SENDER: Recieved Ack " + str(pack) + "\n")
                pack += 1
                window += 1

            if(window == window_size+1):
                window = 1
                if(error_till_now == False):
                    delete_packet(7)
                else:
                    delete_packet(error_pos-1)
                    error_till_now = False
                    pack = pack_error_pos

connection.close()
f.close()
