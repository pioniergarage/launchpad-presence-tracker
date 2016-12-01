import sys
import random
import time

hex_str = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

mac_addresses = []
MAC_ADDRESS_AMOUNT = 20

delta_from = 0.02
delta_to = 1.6

def main():
    gen_mac_addresses(MAC_ADDRESS_AMOUNT)
    try:
        while True:
            delta = random.uniform(delta_from, delta_to)
            print_data()
            time.sleep(delta)
    except (KeyboardInterrupt, SystemExit):
        pass

def print_data():
    line = gen_line()
    sys.stdout.write(line+'\n')

def gen_line():
    mac_address = mac_addresses[random.randint(0,len(mac_addresses)-1)]
    packet_length = (random.randint(0,255) + 128) * 8
    return 'MAC-ADDRESS: {0} LENGHT: {1}'.format(mac_address, packet_length)

def gen_mac_addresses(n):
    for i in range(0,n):
        mac_addresses.append(gen_mac_address())

def gen_mac_address():
    hex_arr = []
    for i in range(0,6):
        j = random.randint(0, 15)
        k = random.randint(0, 15)
        hex_arr.append(hex_str[j] + hex_str[k])
    return ':'.join(hex_arr)

if __name__ == "__main__":
    main()
