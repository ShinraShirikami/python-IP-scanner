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
        return True
    except:
        return False

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
fillQueue(port_list)  # ← FIX: Actually fill the queue
thread_list = []

for t in range(50):  # ← FIX: Reduced from 500
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print("Open ports are:", openPorts)
