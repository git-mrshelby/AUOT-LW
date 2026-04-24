import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# --- Configuration (Professional Gen Coders Brand) ---
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

def send_gen_corders_offer(business_name, owner_email, niche, competitor_site):
    """Sends a high-impact email from Gen Coders Pvt Ltd."""
    business_name = str(business_name).strip()
    niche = str(niche).strip()
    owner_email = str(owner_email).strip()

    if not SMTP_USER or not SMTP_PASS:
        print("Error: SMTP_USER or SMTP_PASS not set in environment.")
        return False

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Audit Report: {business_name} - Why is your competitor closing more clients?"
    msg['From'] = f"Gen Coders <{SMTP_USER}>"
    msg['To'] = owner_email

    # Official Meta-Style Verification Badge (Pure CSS)
    blue_badge = """
    <span style="background-color: #0095f6; color: #fff; border-radius: 50%; display: inline-block; width: 16px; height: 16px; line-height: 16px; text-align: center; font-size: 10px; font-weight: bold; margin-left: 2px; vertical-align: middle;">&#10003;</span>
    """

    # High-End Professional Digital Logo (Transparent Background)
    custom_logo = """
    <div style="background-color: transparent; border: 1px solid #0095f6; border-radius: 50%; width: 65px; height: 65px; display: table; float: right; margin-left: 20px;">
        <div style="display: table-cell; vertical-align: middle; text-align: center; font-family: 'Arial Black', Gadget, sans-serif; line-height: 1.1;">
            <span style="color: #000000; font-size: 9px; letter-spacing: 1px; font-weight: bold;">GEN</span><br>
            <span style="color: #0095f6; font-size: 9px; letter-spacing: 1px; font-weight: bold;">CODERS</span>
        </div>
    </div>
    """

    # Premium Brand Header (Transparent Background)
    brand_header = f"""
    <div style="background-color: transparent; padding: 10px; border-bottom: 2px solid #0095f6; margin-bottom: 15px; text-align: center;">
        <span style="font-family: 'Arial Black', Gadget, sans-serif; font-weight: bold; font-size: 1.2em; letter-spacing: 2px; color: #0095f6;">GEN CODERS {blue_badge}</span>
    </div>
    """

    # Clean Professional Signature (Best Regards - Lead Generation Style)
    signature = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #444; border-top: 1px solid #0095f6; padding-top: 10px; margin-top: 20px; min-height: 100px;">
        {custom_logo}
        <div style="float: left;">
            <span style="font-size: 1.0em; color: #333;">Best Regards,</span><br>
            <span style="font-size: 1.2em; font-weight: bold; color: #000;">Salman Haider {blue_badge}</span><br>
            <span style="font-size: 0.85em; color: #7f8c8d;">Lead Automation Engineer</span><br>
            <strong style="color: #1a1a1a; font-size: 1.0em;">Gen Coders Pvt Ltd {blue_badge}</strong>
        </div>
        <div style="clear: both;"></div>
        <div style="font-size: 0.75em; color: #bdc3c7; font-style: italic; margin-top: 15px; border-top: 1px solid #eee; padding-top: 5px;">
            Global Automation & Revenue Growth Operations
        </div>
    </div>
    """

    display_competitor = "your top local competitor"

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333; font-size: 16px;">
    {brand_header}
    <p>Hi {business_name},</p>
    <p>I was reviewing the local market for <strong>{niche}s</strong> in your area and noticed something critical.</p>
    <p>Your competitor, <strong>{display_competitor}</strong>, has a fully professional website and is currently closing significantly more clients than you because they are visible on Google 24/7.</p>
    <p>You currently have no online presence, which means you are <strong>invisible</strong> to customers searching for your services right now. You are losing money every day.</p>
    <p>At <strong>Gen Coders Pvt Ltd</strong>, we help local businesses dominate their niche. We provide the most affordable and high-quality services in your area. I can send you a <strong>free website sample</strong> for your business tonight if you'd like to see it.</p>
    <p><strong>The Offer:</strong> We only charge <strong>$50 per month</strong> for a professional software solution with <strong>free hosting</strong>. <i>(Custom domain charges are separate)</i>.</p>
    <p>Would you like to see the free sample for {business_name}?</p>
    {signature}
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    msg.attach(part2)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, owner_email, msg.as_string())
            print(f"Gen Coders offer sent to {owner_email}")
            return True
    except Exception as e:
        print(f"Failed to send email to {owner_email}: {e}")
        return False

if __name__ == "__main__":
    # Test execution for the user
    recipient = "mrshelbytrades@gmail.com"
    print(f"Sending polished cold email to {recipient}...")
    send_gen_corders_offer("Shelby's Trading Group", recipient, "Trading Consultant", "TheProTraderNYC.com")
