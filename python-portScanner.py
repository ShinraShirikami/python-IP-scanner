import socket
import threading
from queue import Queue

target = input("Enter the target IP address: ")
queue = Queue()
openPorts = []

def portScan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target, port))
        sock.close()
        try:
            banner = sock.recv(1024).decode().strip()
            sock.close()
            return True, banner
        except:
            sock.close()
            return True, "No banner"
        return True
    except:
        return False, None

def fillQueue(portList):
    for port in portList:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portScan(port):
            print("Port {} is open".format(port))
            openPorts.append(port)

port_list = range(1, 1024)
fillQueue(port_list)
thread_list = []

for t in range(50):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print("Open ports are:", openPorts)

with open('scan_results.txt', 'w') as f:
    f.write(f"Target: {target}\n")
    f.write(f"Open ports found: {len(openPorts)}\n")
    f.write("-" * 30 + "\n")
    for port in openPorts:
        f.write(f"Port {port} is open\n")

print("Results saved to scan_results.txt")
