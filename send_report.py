import requests
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ELASTIC_API_KEY = os.getenv("essu_ZVZnek1HTktkMEpWWVZsbFVUZDBORFkxYW00NlNIbGFRMUEyUlU1TlFWTnFTVTlHY2t0eFFVeHNkdz09AAAAAKKm6O4=")
SENDGRID_API_KEY = os.getenv("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")
SENDER_EMAIL = os.getenv("Diksha.Mohan@sita.aero")
RECIPIENT_EMAIL = os.getenv("Vaishnavi.Omanakuttan@sita.aero")

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

