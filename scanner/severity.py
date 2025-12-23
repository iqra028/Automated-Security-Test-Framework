def port_severity(port):
    if port == 80:
        return "Medium"
    return "Low"

def header_severity(header):
    if header in ["Content-Security-Policy", "Strict-Transport-Security"]:
        return "High"
    return "Medium"
