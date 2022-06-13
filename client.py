import socket
import sys
import ipaddress



if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    if type(ipaddress.ip_address(HOST)) == ipaddress.IPv4Address:
        AF = socket.AF_INET
    else:
        AF = socket.AF_INET6
    
    with socket.socket(AF, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            msg = input().encode('ascii', 'ignore')
            s.sendall(msg)
            
            recv_data = s.recv(500)
            if not recv_data:
                s.close()
                break
            recv_msg = recv_data.decode()
            print(f"received {recv_msg}")