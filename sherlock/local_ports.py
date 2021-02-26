import socket
import time

#Create socket and attempt to connect to local ports.
#connect_ex returns error code for failtures to connect, so 0 == open.
#return open ports as a list
#0-1024 default range 'well known ports'
def local_port_scan(end_port=1024):
    start = time.time()
    open_ports = []

    for port in range(0,end_port):
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex(("127.0.0.1", port))

        if result == 0:
            open_ports.append(port)
        test_socket.close()
    end = time.time()

    print("run time: ", end - start)
    return open_ports
