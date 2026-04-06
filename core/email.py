import os
import smtplib
from email.message import EmailMessage

def send_recommendation_email(recommendation_text):
    """Sends the LLM's recommendation via email to a list of clients."""
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    client_emails_str = os.getenv("CLIENT_EMAILS")
    
    if not all([sender_email, sender_password, client_emails_str]):
        print("Email credentials or client list missing in .env file.")
        return False

    client_list = [email.strip() for email in client_emails_str.split(",")]

    # --- THE CLEANUP FIX ---
    # Strip out any markdown backticks the LLM might have stubbornly included
    clean_html = recommendation_text.replace("```html", "").replace("```", "").strip()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        
        for client_email in client_list:
            msg = EmailMessage()
            msg['Subject'] = "🏔️ Your Daily Hiking Recommendation"
            msg['From'] = sender_email
            msg['To'] = client_email
            
            # --- THE RENDERING FIX ---
            # Using set_content with subtype='html' forces the email client to render the code
            msg.set_content(clean_html, subtype='html')
            
            server.send_message(msg)
            print(f"Success: Email sent to {client_email}!")
            
        server.quit()
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False