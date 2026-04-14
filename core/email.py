import os
import smtplib
from email.message import EmailMessage

def send_recommendation_email(recommendation_text):
    """Sends the LLM's recommendation via email to subscribers in the CSV file."""
    
    # 1. Credentials still come from .env (Security Best Practice)
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    # 2. Path Logic: Find subscribers.csv in the same folder as this script
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, '../subscribers.csv')
    
    # 3. Validation Check
    if not all([sender_email, sender_password]):
        print("Error: Email credentials missing in .env file.")
        return False

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. No one to email!")
        return False

    # 4. Load the subscriber list from the CSV
    client_list = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        # Assuming one email per line (as written by your Streamlit app)
        client_list = [line.strip() for line in f if line.strip()]

    if not client_list:
        print("Subscriber list is empty. Skipping email broadcast.")
        return False

    # 5. Cleanup the LLM Markdown
    clean_html = recommendation_text.replace("```html", "").replace("```", "").strip()

    try:
        # Using Gmail's SSL port
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        
        for client_email in client_list:
            msg = EmailMessage()
            msg['Subject'] = "🏔️ Your Daily Hiking Recommendation"
            msg['From'] = f"Hiking Agent <{sender_email}>" # Added a display name
            msg['To'] = client_email
            
            # Set HTML content for rendering
            msg.set_content(clean_html, subtype='html')
            
            server.send_message(msg)
            print(f"Success: Report delivered to {client_email}")
            
        server.quit()
        return True
        
    except Exception as e:
        print(f"Failed to broadcast emails: {e}")
        return False