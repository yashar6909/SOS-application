from flask import Flask, request, jsonify
import smtplib
import requests

app = Flask(__name__)

# Email configuration
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_SMTP_SERVER = "smtp.example.com"  # e.g., smtp.gmail.com
EMAIL_SMTP_PORT = 587  # Use 587 for TLS or 465 for SSL
RECIPIENT_EMAIL = "recipient@example.com"

# Slack Webhook URL (Replace this with your actual Slack Webhook URL)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/slack/webhook"

def send_email(subject, body):
    """
    Sends an email with the given subject and body.
    """
    try:
        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message)
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_slack_message(message):
    """
    Sends a message to Slack using an incoming webhook.
    """
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if response.status_code == 200:
            print("Slack message sent successfully")
            return True
        else:
            print(f"Failed to send Slack message: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending Slack message: {e}")
        return False

@app.route("/sos", methods=["POST"])
def handle_sos():
    """
    Endpoint to handle incoming SOS requests.
    """
    data = request.json
    message = data.get("message", "SOS Alert!")
    ip_address = data.get("ip_address")
    workstation_name = data.get("workstation_name")
    current_user = data.get("current_user")

    # Prepare the notification message
    notification_message = (
        f"SOS Alert triggered!\n"
        f"Message: {message}\n"
        f"IP Address: {ip_address}\n"
        f"Workstation Name: {workstation_name}\n"
        f"Current User: {current_user}"
    )

    # Send Email Notification
    email_subject = "SOS Alert from Workstation"
    if send_email(email_subject, notification_message):
        email_status = "Email sent successfully"
    else:
        email_status = "Failed to send email"

    # Send Slack Notification
    if send_slack_message(notification_message):
        slack_status = "Slack notification sent successfully"
    else:
        slack_status = "Failed to send Slack notification"

    # Respond to the SOS request
    return jsonify({
        "status": "SOS notification received",
        "email_status": email_status,
        "slack_status": slack_status
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
