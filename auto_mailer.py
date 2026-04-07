import smtplib
from email.message import EmailMessage
import os

# --- Configuration (Free Tier Stack) ---
# Use SendGrid, Mailgun, or just a free Gmail account with App Password.
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = os.environ.get("SMTP_PORT", 587)
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

def send_automation_email(to_email, niche, leads_sample):
    """Send a cold-email with a lead sample to target marketing agencies"""
    
    msg = EmailMessage()
    msg.set_content(f"""Hi [Name],

I'm a software engineer. I built a bot that finds businesses in {niche} in Chicago that are ready for marketing/revamp. 

I have 100 fresh leads from this week. Here are 3 for free to test:
{leads_sample}

If you close any of these, keep the money! If you'd like my bot to send you the full list every Monday morning, it's just $49/month via subscription.

Let me know if you want the link.

Best,
[Your Name]
""")

    msg['Subject'] = f"100 {niche} Leads for your Agency (Chicago)"
    msg['From'] = SMTP_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example usage: Find an agency and send them a sample
    # (Automate this by scraping 'Marketing Agency' leads first)
    print("Auto-Mailer ready. Configuration required.")
