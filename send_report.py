import requests
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def fetch_eci_usage():
    url = "https://api.elastic-cloud.com/api/v1/billing/costs/organizations"
    headers = {"Authorization": f"ApiKey {ELASTIC_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    total_eci = data["costs"]["total"]["ecu"]
    return total_eci

def send_email(report):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECIPIENT_EMAIL,
        subject="Weekly Elastic ECU Usage Report",
        html_content=f"<pre>{report}</pre>"
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)

def main():
    total_eci = fetch_eci_usage()

    report = f"""
Weekly Elastic ECU Usage Report
Date: {datetime.utcnow().strftime('%Y-%m-%d')}

Total ECU consumed so far: {total_eci}

Regards,
Automated Report
"""

    send_email(report)

if __name__ == "__main__":
    main()
