import socket

def scan_ports(target, allowed_ports):
    detected = []

    for port in [21, 22, 23, 80, 443, 3306]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((target, port)) == 0:
            if port not in allowed_ports:
                detected.append(port)
        sock.close()

    return detected
