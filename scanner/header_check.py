import requests

def check_headers(url, required_headers):
    response = requests.get(url, timeout=5)
    missing = []

    for header in required_headers:
        if header not in response.headers:
            missing.append(header)

    return missing
