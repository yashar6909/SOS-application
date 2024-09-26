import socket
import smtplib
import requests
from cryptography.fernet import Fernet

# AES Encryption Key (Must be the same as the one on the client)
KEY = b'your_32_byte_secret_key_here'  # Ensure this key is 32 bytes long
cipher_suite = Fernet(KEY)

# Email configuration
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_SMTP_SERVER = "smtp.example.com"  # e.g., smtp.gmail.com
EMAIL_SMTP_PORT = 587  # Use 587 for TLS or 465 for SSL
RECIPIENT_EMAIL = "recipient@example.com"

# Slack Webhook URL (Replace this with your actual Slack Webhook URL)
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/slack/webhook"

def decrypt_data(encrypted_data):
    """
    Decrypt the given data using AES (Fernet) decryption.
    """
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return eval(decrypted_data.decode('utf-8'))  # Convert back to dictionary

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

def handle_sos(data):
    """
    Handle the decrypted SOS alert by sending a Slack message and an email notification.
    """
    decrypted_data = decrypt_data(data)
    message = decrypted_data.get("message", "SOS Alert!")
    ip_address = decrypted_data.get("ip_address")
    workstation_name = decrypted_data.get("workstation_name")
    current_user = decrypted_data.get("current_user")

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

    print(f"Notification Results: {email_status}, {slack_status}")

def start_server():
    """
    Start the UDP server to listen for incoming SOS alerts.
    """
    server_ip = "0.0.0.0"  # Listen on all network interfaces
    server_port = 5000

    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((server_ip, server_port))
        print(f"Server listening on {server_ip}:{server_port} for UDP packets")

        while True:
            # Receive the data (UDP is connectionless, so there's no connection accept)
            data, client_address = server_sock.recvfrom(1024)  # Buffer size
            print(f"Received SOS from {client_address}")
            if data:
                handle_sos(data)

if __name__ == "__main__":
    start_server()
