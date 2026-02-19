import requests
import os
import csv
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SESSION_COOKIE = os.getenv("ELASTIC_SESSION_COOKIE")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

ORG_ID = "1927158194"  # Your org ID from the URL

def get_month_range():
    """Return first and last day of the current month in ISO format."""
    today = datetime.utcnow()
    first_day = today.replace(day=1)
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    last_day = next_month - timedelta(seconds=1)

    return (
        first_day.strftime("%Y-%m-%dT00:00:00Z"),
        last_day.strftime("%Y-%m-%dT23:59:59Z"),
    )

def download_csv():
    start, end = get_month_range()

    url = (
        f"https://cloud.elastic.co/api/v2/billing/organizations/{ORG_ID}/costs/items"
        f"?from={start}&to={end}&serverless_group_by=product_family"
    )

    cookies = {"__ec_session": SESSION_COOKIE}

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    return response.content.decode("utf-8")

def parse_eci_from_csv(csv_text):
    total_eci = 0.0

    reader = csv.DictReader(csv_text.splitlines())
    for row in reader:
        # Column name in Elastic CSV is usually "total" or "ecu"
        for key in row:
            if "ecu" in key.lower() or "total" in key.lower():
                try:
                    total_eci += float(row[key])
                except:
                    pass

    return round(total_eci, 4)

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
    csv_text = download_csv()
    total_eci = parse_eci_from_csv(csv_text)

    report = f"""
Weekly Elastic ECU Usage Report
Date: {datetime.utcnow().strftime('%Y-%m-%d')}

Reporting period: Current calendar month
Total ECU consumed so far: {total_eci}

Regards,
Automated Report
"""

    send_email(report)

if __name__ == "__main__":
    main()
