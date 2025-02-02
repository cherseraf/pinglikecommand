# A ping-like Command
A ping-like script that sends ICMP packets to the specified IP address.

Usage: ping.py [-h] [-i I] [-w W] [-S S] [-t] [-n N] target_ip

A ping-like script that sends ICMP packets to the specified IP address.

positional arguments:
  target_ip   Target IP address (IPv4 or IPv6)

options:
  -h, --help:  show this help message and exit
  -i I:        TTL value
  -w W:        Timeout in milliseconds to wait for each reply
  -S S:        Source address to use
  -t:          Ping until stopped (Ctrl+C to stop)
  -n N:        Number of ICMP packets to be sent
