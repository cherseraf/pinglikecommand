from scapy.all import *
import argparse
import socket
import sys
import time

def send_ping(target_ip, ttl, timeout, source_addr=None, continuous=False, num_of_packets=4):

    print("Pinging " + target_ip)

    try:
        packets_sent = 0
        packets_received = 0
        minimum_time = 0
        maximum_time = 0
        average_time = 0
        temp = 0
        
        while(temp < num_of_packets):
            packet = IP(dst=target_ip, src=source_addr, ttl=ttl)/ICMP()/"abcdefghijklmnopqrstuvwabcdefghi"

            response = sr1(packet, timeout=timeout)
            packets_sent += 1
            temp = packets_sent

            if response:
                time = (response.time - packet.sent_time) * 1000
                if(packets_sent == 1):
                    average_time = time
                else:
                    average_time = (average_time + time) / 2 

                if int(time) == 0:
                    print(f"Reply from {target_ip}: time<1ms TTL={response[IP].ttl}")
                else:
                    print(f"Reply from {target_ip}: time={int(time)}ms TTL={response[IP].ttl}")

                packets_received += 1
                if(time < minimum_time):
                    minimum_time = time
                if(time > maximum_time):
                    maximum_time = time

            else:
                print(f"Reply from {target_ip}: Destination host unreachable.")

            if continuous:
                temp = 0
                

        if(packets_sent > 0):
            lost_packets = packets_sent - packets_received
            packet_loss = int(lost_packets/packets_sent)*100
            print(f"\nPing statics for {target_ip}:")
            print(f"\tPackets: Sent = {packets_sent}, Received = {packets_received}, Lost = {lost_packets} ({packet_loss}% loss),\n")

    except KeyboardInterrupt:
        lost_packets = packets_sent - packets_received
        packet_loss = int(lost_packets/packets_sent)*100
        print(f"\nPing statics for {target_ip}:")
        print(f"\tPackets: Sent = {packets_sent}, Received = {packets_received}, Lost = {lost_packets} ({packet_loss})% loss),")
        if(packets_received>0):
            print("\nApproximate round trip times in milli-seconds:")
            print(f"\tMinimum = {int(minimum_time)}ms, Maximum = {int(maximum_time)}ms, Average = {int(average_time)}ms\n")
        print("\nKeyboar")

def main():
    parser = argparse.ArgumentParser(description="A ping-like script that sends ICMP packets to the specified IP address.")
    parser.add_argument("target_ip", type=str, help="Target IP address (IPv4 or IPv6)")
    parser.add_argument("-i", type=int, default=128, help="TTL value")
    parser.add_argument("-w", type=int, default=1000, help="Timeout in milliseconds to wait for each reply")
    parser.add_argument("-S", type=str, help="Source address to use")
    parser.add_argument("-t", action="store_true", help="Ping until stopped (Ctrl+C to stop)")
    parser.add_argument("-n", type=int, default=4, help="Number of ICMP packets to be sent")

    args = parser.parse_args()

    timeout = args.w / 1000
    continuous = args.t
    num_of_packets = 0
    source_addr=args.S
    ttl = args.i
    target_ip = args.target_ip

    if continuous:
        num_of_packets = sys.maxsize
    else:
        num_of_packets = args.n

    send_ping(
        target_ip,
        ttl,
        timeout,
        source_addr,
        continuous,
        num_of_packets
    )

if __name__ == "__main__":
    main()
