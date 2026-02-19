import requests
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SESSION_COOKIE = os.getenv("ELASTIC_SESSION_COOKIE")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def fetch_eci_usage():
    url = "https://cloud.elastic.co/api/v1/billing/usage"  # Internal UI API
    cookies = {"__ec_session": SESSION_COOKIE}

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()
    data = response.json()

    # Extract ECU usage from internal API
    total_eci = data.get("totalEcu", 0)
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
