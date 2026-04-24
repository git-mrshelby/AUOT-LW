import smtplib
from email.message import EmailMessage
import os
import csv

# --- Configuration ---
# Your direct email template for business owners
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

def send_direct_audit_email(business_name, owner_email, website, issue):
    """Send a direct email to a business owner with their specific 'Service Gap'"""
    
    msg = EmailMessage()
    
    # Dynamic email content based on the issue found
    if issue == 'has_slow_heuristic':
        body = f"""Hi {business_name},

I was browsing your website ({website}) and noticed it takes over 5 seconds to load on my mobile phone. 

I'm a local software engineer, and I want to fix this for you. Most businesses lose 50% of their customers if their site is slow. 

I've already built a faster version of your site that loads in under 1 second. Would you like to see the performance comparison? No obligation.

Best,
[Your Name]
"""
    elif issue == 'has_mobile_issue':
        body = f"""Hi {business_name},

I noticed your website ({website}) is not optimized for mobile phones. It's very difficult for customers to click your 'Call' or 'Contact' buttons on smaller screens.

I can fix this in one afternoon. Mobile-friendly sites get 2x more calls than ones that aren't.

Would you like me to send you a 1-minute video showing the fix?

Best,
[Your Name]
"""
    else: # Default/SSL issue
        body = f"""Hi {business_name},

I noticed your website ({website}) shows a 'Not Secure' warning in Google Chrome. Many customers will see this and immediately leave your site out of fear.

I can fix this for you today so the green padlock appears and your visitors feel safe.

Let me know if you want me to handle it for you.

Best,
[Your Name]
"""

    msg.set_content(body)
    msg['Subject'] = f"Quick Question about {business_name}'s website"
    msg['From'] = SMTP_USER
    msg['To'] = owner_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print(f"Direct audit email sent to {owner_email}")
    except Exception as e:
        print(f"Failed to send direct email: {e}")

if __name__ == "__main__":
    # Example logic: Read the audit results and send emails to anyone with a slow site
    # (Automate this by reading audit_results.csv)
    print("Direct Auto-Mailer ready. Configuration required.")
