import ssl
import socket

def check_ssl(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                return "SSL Enabled"
    except:
        return "SSL Not Configured"
