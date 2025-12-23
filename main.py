import argparse
import yaml
import json
from scanner.port_scan import scan_ports
from scanner.header_check import check_headers
from scanner.ssl_check import check_ssl
from scanner.severity import port_severity, header_severity


parser = argparse.ArgumentParser(description="Automated Security Test Framework")
parser.add_argument("--target", required=True, help="Target domain/IP")
parser.add_argument("--url", required=True, help="Target URL")
args = parser.parse_args()

with open("baseline.yaml") as f:
    baseline = yaml.safe_load(f)

open_ports = scan_ports(args.target, baseline["allowed_ports"])
missing_headers = check_headers(args.url, baseline["required_headers"])
ssl_status = check_ssl(args.target)

report = {
    "port_scan": {
        "status": "FAIL" if open_ports else "PASS",
        "severity": {p: port_severity(p) for p in open_ports},
        "open_ports": open_ports
    },
    "headers": {
        "status": "FAIL" if missing_headers else "PASS",
        "severity": {h: header_severity(h) for h in missing_headers},
        "missing_headers": missing_headers
    },
    "ssl": {
        "status": "PASS" if ssl_status == "SSL Enabled" else "FAIL"
    }
}

# Write JSON report
with open("reports/report.json", "w") as jf:
    json.dump(report, jf, indent=4)

# Write text report
with open("reports/report.txt", "w") as tf:
    tf.write("=== Security Test Execution Report ===\n\n")

    tf.write("[Port Scan]\n")
    tf.write(f"Status: {report['port_scan']['status']}\n")
    tf.write(f"Findings: {open_ports}\n\n")

    tf.write("[HTTP Headers]\n")
    tf.write(f"Status: {report['headers']['status']}\n")
    tf.write(f"Missing: {missing_headers}\n\n")

    tf.write("[SSL]\n")
    tf.write(f"Status: {report['ssl']['status']}\n")
