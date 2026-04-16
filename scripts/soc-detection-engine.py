import re
import json
from collections import defaultdict
from datetime import datetime

log_file = "../logs/sample_auth.log"

failed_logins = defaultdict(list)
successful_logins = defaultdict(int)
user_attempts = defaultdict(set)

THRESHOLD = 5
TIME_WINDOW = 60  # seconds

alerts = []

print("[+] Starting SOC Level 2 detection...")

try:
    with open(log_file, "r") as file:
        for line in file:

            ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
            user_match = re.search(r'for (invalid user )?(\w+)', line)

            if ip_match:
                ip = ip_match.group(1)

                timestamp = datetime.now()  # simulate timestamp

                # Failed logins
                if "Failed password" in line:
                    failed_logins[ip].append(timestamp)

                    if user_match:
                        user = user_match.group(2)
                        user_attempts[ip].add(user)

                # Successful logins
                if "Accepted password" in line:
                    successful_logins[ip] += 1

    print("\n[+] Detection Results:\n")

    with open("../output/alerts.json", "w") as json_file:

        for ip in failed_logins:

            fail_count = len(failed_logins[ip])
            unique_users = len(user_attempts[ip])

            risk_score = 0
            severity = "LOW"
            alert_type = ""

            # Brute Force
            if fail_count >= THRESHOLD:
                risk_score += 40
                alert_type = "Brute Force"

            # Password Spraying
            if unique_users >= 5:
                risk_score += 30
                alert_type = "Password Spraying"

            # Success After Failure
            if successful_logins[ip] > 0 and fail_count >= THRESHOLD:
                risk_score += 50
                alert_type = "Account Compromise"

            # Severity Mapping
            if risk_score >= 80:
                severity = "CRITICAL"
            elif risk_score >= 50:
                severity = "HIGH"
            elif risk_score >= 30:
                severity = "MEDIUM"

            if risk_score > 0:
                alert = {
                    "ip": ip,
                    "failed_attempts": fail_count,
                    "unique_users": unique_users,
                    "successful_logins": successful_logins[ip],
                    "alert_type": alert_type,
                    "severity": severity,
                    "risk_score": risk_score,
                    "timestamp": str(datetime.now())
                }

                alerts.append(alert)

                print(f"[{severity}] {alert_type} detected from {ip} (Risk Score: {risk_score})")

        json.dump(alerts, json_file, indent=4)

    print("\n[+] Analysis complete. Alerts saved to output/alerts.json")

except FileNotFoundError:
    print("[ERROR] Log file not found. Please check the path.")
