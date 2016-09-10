# Server to receive messages over Simple Transport Protocol (STP). The server 
# sits in an infinite loop listening for a file in sent via UDP packets from 
# an STP client. The server then reassembles the data and writes it to file 
# under the user-specified filename.
#
# Written by Juliana Zhu, z3252163
# Written for COMP9331 16s2, Assignment 1. 
#
# Python 3.0


import sys
import socket
import datetime
import time
from stp_headers import receive_segment     # helper
from stp_headers import create_header       # helper
from stp_headers import interpret_header    # helper


RECEIVER_IP = "127.0.0.1"


def send_SYNACK(return_addr, received_sequence_number, sequence_number):
    print("Received Sequence Number:", received_sequence_number)
    ack_number = received_sequence_number + 1 
    header = create_header("SYNACK", sequence_number, ack_number)
    segment = header
    sock.sendto(segment, (return_addr))

def receive_ACK(expected_ack):
    return_addr, segment_type, received_sequence_no, received_ack_no, data = receive_segment(sock)
    if segment_type == "ACK" and received_ack_no == expected_ack:
        return return_addr, received_sequence_no, received_ack_no
    else:
        receive_ACK(expected_ack)

def receive_data(expected_ack):
    assembled_file = "" 
    while True:
        return_addr, segment_type, received_sequence_no, received_ack_no, data = receive_segment(sock)
        print("expected_ack= {}, received_ack_no= {}".format(expected_ack, received_ack_no))
        if segment_type == "PUSH" and received_ack_no == expected_ack:
            assembled_file += data.decode("ascii")
            send_ACK(return_addr, received_sequence_no, received_ack_no)
            expected_ack = received_ack_no
        elif segment_type == "FIN":
            try:
                with open(filename, 'a') as f:
                    f.write(assembled_file)
                    f.close()
            except OSError:
                print("File already exists. Exiting.")
                sys.exit()
            return return_addr, received_sequence_no, received_ack_no
        print("--------------------------------------")


def send_ACK(return_addr, ack_number, sequence_number):
    segment = create_header("ACK", sequence_number, ack_number)
    sock.sendto(segment, (return_addr))
    print("Just sent the ACK of sequence_number {} and ack {}:".format(sequence_number, ack_number))

def send_FIN(return_addr, sequence_number, ack_number):
    segment = create_header("FIN", sequence_number, ack_number)
    sock.sendto(segment, (return_addr))
    print("Just sent the FIN of sequence_number {} and ack {}:".format(sequence_number, ack_number+1))

# ===== MAIN =====
# Command line arguments
try:
    receiver_port = int(sys.argv[1])
    filename = sys.argv[2]
except (IndexError, ValueError):
    print("Incorrect arguments. Usage: receiver.py <receiver_port> <file.txt>")
    sys.exit()

# Open the listening socket port.
sock = socket.socket(socket.AF_INET,                # internet
                            socket.SOCK_DGRAM)      # UDP
sock.bind((RECEIVER_IP, receiver_port))
sequence_number = 0 # Temp => change to random no. after testing
return_addr, segment_type, received_sequence_no, received_ack_no, data = receive_segment(sock)
send_SYNACK(return_addr, received_sequence_no, sequence_number)
sequence_number += 1
return_addr, received_sequence_no, received_ack_no = receive_ACK(sequence_number)
print("Successfully received ACK")
# Receives all PUSH segments from sender, then 
# Returns the segment details of the FIN received:
return_addr, received_sequence_no, received_ack_no = receive_data(sequence_number)
received_sequence_no += 1
send_ACK(return_addr, received_ack_no, received_sequence_no)
print("Just sent second last ACK")
received_sequence_no += 1
send_FIN(return_addr, received_sequence_no, received_ack_no)
print("sent last FIN")
receive_ACK(received_sequence_no + 1)
print("All done, terminating")
sock.close()