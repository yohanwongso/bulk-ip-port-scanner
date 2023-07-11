import socket
import csv
from re import findall
from subprocess import Popen, PIPE

def ping (ip,ping_count):
    data = ""
    output= Popen(f"ping {ip} -n {ping_count}", stdout=PIPE, encoding="utf-8")

    for line in output.stdout:
        data = data + line
        ping_test = findall("TTL=", data)

    if ping_test:
        return True
    else:
        return False

list_ip_file = open("ip.txt", "r")
list_port_file = open("port.txt", "r")

ports = []
csv_header = ["IP", "Ping"]

for port_with_enter in list_port_file:
    port = int(port_with_enter.replace("\n", ""))
    ports.append(port)
    csv_header.append(port)

with open('report.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)

    for ip_with_enter in list_ip_file:
        ip = ip_with_enter.replace("\n", "")
        
        if ping (ip, 1) == True:
            ping_result = "Accessible"
        else:
            ping_result = "Not accessible"
        
        csv_data = [ip, ping_result]

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            result = sock.connect_ex((ip,port))
            if result == 0:
                csv_data.append("Accessible")
                print (ip, "\t", port, "\tAccessible")
            else:
                csv_data.append("Not accessible")
                print (ip, "\t", port, "\tNot accessible")
            sock.close()

        writer.writerow(csv_data)

f.close()
