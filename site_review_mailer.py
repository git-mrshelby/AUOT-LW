import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# --- Configuration (Professional Gen Coders Brand) ---
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

def send_site_review(recipient_email, site_url):
    """Sends a professional site review email from Gen Coders."""
    
    if not SMTP_USER or not SMTP_PASS:
        print("Error: SMTP_USER or SMTP_PASS not set in environment.")
        return False

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Site Audit Report: Louis Pest Control - Premium Build Review"
    msg['From'] = f"Gen Coders <{SMTP_USER}>"
    msg['To'] = recipient_email

    # Official Meta-Style Verification Badge (Pure CSS)
    blue_badge = """
    <span style="background-color: #0095f6; color: #fff; border-radius: 50%; display: inline-block; width: 16px; height: 16px; line-height: 16px; text-align: center; font-size: 10px; font-weight: bold; margin-left: 2px; vertical-align: middle;">&#10003;</span>
    """

    # High-End Professional Digital Logo
    custom_logo = """
    <div style="background-color: transparent; border: 1px solid #0095f6; border-radius: 50%; width: 65px; height: 65px; display: table; float: right; margin-left: 20px;">
        <div style="display: table-cell; vertical-align: middle; text-align: center; font-family: 'Arial Black', Gadget, sans-serif; line-height: 1.1;">
            <span style="color: #000000; font-size: 9px; letter-spacing: 1px; font-weight: bold;">GEN</span><br>
            <span style="color: #0095f6; font-size: 9px; letter-spacing: 1px; font-weight: bold;">CODERS</span>
        </div>
    </div>
    """

    # Premium Brand Header
    brand_header = f"""
    <div style="background-color: transparent; padding: 10px; border-bottom: 2px solid #0095f6; margin-bottom: 15px; text-align: center;">
        <span style="font-family: 'Arial Black', Gadget, sans-serif; font-weight: bold; font-size: 1.2em; letter-spacing: 2px; color: #0095f6;">GEN CODERS {blue_badge}</span>
    </div>
    """

    # Clean Professional Signature
    signature = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #444; border-top: 1px solid #0095f6; padding-top: 10px; margin-top: 20px; min-height: 100px;">
        {custom_logo}
        <div style="float: left;">
            <span style="font-size: 1.0em; color: #333;">Best Regards,</span><br>
            <span style="font-size: 1.2em; font-weight: bold; color: #000;">S . Mohsin {blue_badge}</span><br>
            <span style="font-size: 0.85em; color: #7f8c8d;">Lead Automation Engineer</span><br>
            <strong style="color: #1a1a1a; font-size: 1.0em;">Gen Coders Pvt Ltd {blue_badge}</strong>
        </div>
        <div style="clear: both;"></div>
        <div style="font-size: 0.75em; color: #bdc3c7; font-style: italic; margin-top: 15px; border-top: 1px solid #eee; padding-top: 5px;">
            Global Automation & Revenue Growth Operations
        </div>
    </div>
    """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; font-size: 16px;">
    {brand_header}
    <p>Hi,</p>
    <p>I’ve completed a thorough review of the pest control site you built here: <a href="{site_url}" style="color: #0095f6; text-decoration: none; font-weight: bold;">{site_url}</a></p>
    
    <p><strong>Review Summary:</strong></p>
    <ul style="list-style-type: square; color: #444;">
        <li><strong>Aesthetics:</strong> The dark-themed design with neon accents looks very modern and professional. It definitely has that "premium" feel.</li>
        <li><strong>Performance:</strong> The site loads fast, which is critical for local service SEO.</li>
        <li><strong>Responsiveness:</strong> Tested on multiple screen sizes; the layout holds up perfectly on mobile.</li>
        <li><strong>Optimization:</strong> Call-to-action buttons are well-placed and highly visible.</li>
    </ul>

    <p><strong>Required Fixes:</strong><br>
    I noticed some <strong>placeholder data</strong> that needs updating before we go live (e.g., "Address: Mars" and "Phone: +1 111 111 1111").</p>

    <p><strong>Next Steps:</strong><br>
    If you want to proceed with connecting this to a <strong>custom domain</strong>, setting up <strong>hosting/maintenance</strong>, and discussing <strong>service charges</strong>, let’s connect further.</p>
    
    <p style="background: #f4f4f4; padding: 15px; border-left: 5px solid #0095f6; font-weight: bold;">
        Telegram: <a href="https://t.me/gencodersofficial" style="color: #0095f6; text-decoration: none;">@gencodersofficial</a>
    </p>

    <p>Looking forward to scaling this further!</p>
    {signature}
    </body>
    </html>
    """

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, recipient_email, msg.as_string())
            print(f"Site review sent to {recipient_email}")
            return True
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")
        return False

if __name__ == "__main__":
    target = "mrshelbytrades@gmail.com"
    site = "https://louispestcontrol.netlify.app/"
    send_site_review(target, site)
