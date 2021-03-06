#!/usr/bin/python3 -u
#
# This module implements a log for Simple Transport Protocol (STP) Senders
# and Receivers. 
#
# Written by Juliana Zhu, z3252163 
# Written for COMP9331 16s2, Assignment 1. 
#
# Python 3.0


from segment import Segment
from datetime import datetime


class Log:

    def __init__(self, filename, start_time):
        self.filename = filename
        self.start = start_time

        self.bytes_transferred = 0
        self.data_segments_sent = 0
        self.packets_dropped = 0
        self.packets_retransmitted = 0
        self.duplicate_acks = 0
        self.bytes_received = 0
        self.data_segments_received = 0
        self.duplicate_segments = 0

        open(self.filename, 'w').close()

    def update(self, entry_type, segment):
        if entry_type == 'drop':
            self.packets_dropped += 1
        elif entry_type == 'ret':
            self.packets_retransmitted += 1

        if entry_type == 'ret':
            entry_type = 'snd'
        code = '{:>8}'.format(segment.type)
        sequence_number = '{:6}'.format(int(segment.sequence))
        data_length = '{:6}'.format(len(segment.data))
        ack_number = '{:6}'.format(int(segment.ack))
        log_entry = '{:6}'.format(entry_type) + self.time_since_start(segment) + code + sequence_number + data_length + ack_number + '\n'
        with open(self.filename, 'a') as f:
            f.write(log_entry)
            f.close()
        return

    def time_since_start(self, segment):
        segment_time = datetime.now()
        diff = segment_time - self.start
        millisecond_diff = diff.seconds * 1000 + diff.microseconds / 1000.0
        print("DIFF = ", millisecond_diff)
        return '{:8}'.format(str(round(millisecond_diff, 2)))

    def sender_close(self):
        log_entry = ""
        log_entry += "Amount of Data Transferred (in bytes): {} \n".format(self.bytes_transferred)
        log_entry += "Number of Data Segments Sent (excluding retransmissions): {} \n".format(self.data_segments_sent)
        log_entry += "Number of Packets Dropped: {} \n".format(self.packets_dropped)
        log_entry += "Number of Retransmitted Segments: {} \n".format(self.packets_retransmitted)
        log_entry += "Number of Duplicate Acknowledgements received: {} \n".format(self.duplicate_acks)        
        with open(self.filename, 'a') as f:
            f.write(log_entry)
            f.close()

    def receiver_close(self):
        log_entry = ""
        log_entry += "Amount of Data Received (in bytes): {} \n".format(self.bytes_received)
        log_entry += "Number of Data Segments Received: {} \n".format(self.data_segments_received)
        log_entry += "Number of Duplicate Segments received: {} \n".format(self.duplicate_segments)        
        with open(self.filename, 'a') as f:
            f.write(log_entry)
            f.close()