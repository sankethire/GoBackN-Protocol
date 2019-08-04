import socket
import time
import random

open('reciever_log.txt', 'a+w').close()
f = open("reciever_log.txt", 'r+b')

error_prob = 0.01
window_size = 7
prop_delay = 0.1

def time_delay(delay):
	if(delay == -1):
		sleep_time = random.randint(0,5)*0.001
		time.sleep(sleep_time)
	else:
		time.sleep(delay)

s = socket.socket()
host = socket.gethostname()
port = 8009
s.connect((host,port))

sender_test = s.recv(20)
print(sender_test)
s.send("Reciever Connected! Send some packets now...")

pack = 1
window = 1
error_till_now = False

while(True):
	while(window <= window_size):
		
		time_delay(prop_delay)
		packet = s.recv(285)
		
		if(error_till_now == False):
			if(packet[0:32] == "**32*BYTES*HEADER*HAS*ERRORS*1**"):
				print("RECIEVER: Recieved Packet " + str(pack) + " (error)")
				f.write("RECIEVER: Recieved Packet " + str(pack) + " (error) \n")
				# print("ack: ***32*BYTES*ACKN*HAS*ERRORS*1***")
				s.send("***32*BYTES*ACKN*HAS*ERRORS*1***") #NACK
				print("RECIEVER: Sending Ack " + str(pack) + " (error). Asking Sender to Go-Back-N to packet " + str(pack))
				f.write("RECIEVER: Sending Ack " + str(pack) + " (error). Asking Sender to Go-Back-N to packet " + str(pack) + "\n")
				error_till_now = True

			else:
				error_new = random.randint(1,20)
				if(error_new == 1):
					print("RECIEVER: Recieved Packet " + str(pack))
					f.write("RECIEVER: Recieved Packet " + str(pack) + "\n")
					# print("ack: ***32*BYTES*ACKN*HAS*ERRORS*1***")
					s.send("***32*BYTES*ACKN*HAS*ERRORS*1***") #ACK
					print("RECIEVER: Sending Ack " + str(pack) + " (error). Asking Sender to Go-Back-N to packet " + str(pack))
					f.write("RECIEVER: Sending Ack " + str(pack) + " (error). Asking Sender to Go-Back-N to packet " + str(pack) + "\n")
					error_till_now = True
				else:
					print("RECIEVER: Recieved Packet " + str(pack))
					f.write("RECIEVER: Recieved Packet " + str(pack) + "\n")
					# print("ack: ***32*BYTES*ACKN*HAS*ERRORS*0***")
					s.send("***32*BYTES*ACKN*HAS*ERRORS*0***") #ACK
					print("RECIEVER: Sending Ack " + str(pack))
					f.write("RECIEVER: Sending Ack " + str(pack) + "\n")
					pack = pack + 1
		window += 1

	if(window == window_size + 1):
		error_till_now = False
		window = 1

s.close()
f.close()