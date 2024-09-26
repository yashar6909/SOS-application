# SOS Notification System

This project implements an SOS notification system that allows workstations to send emergency alerts to a central server. The central server can then send notifications via email or Slack. This system is useful for environments where quick alerts and notifications are necessary.

## Features

- **SOS Button Application**: A Python-based desktop application that displays a button on Windows desktops. When clicked, it sends an SOS alert to the central server.
- **Central Server**: A Python Flask-based server that listens for SOS alerts and sends notifications via:
  - **Email** (using SMTP)
  - **Slack** (using an incoming webhook)
- **Workstation Information**: The SOS alert includes the workstation's IP address, hostname, and currently logged-in user.

## Technologies Used

- **Python**: Core programming language for both client and server.
- **Flask**: Web framework for building the central server.
- **SMTP**: For sending email notifications.
- **Slack Webhooks**: For sending notifications to a Slack channel.

## Requirements

- Python 3.x
- Pip for installing dependencies

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yashar6909/sos-application.git
cd sos-notification-system

2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Configure the Server
Edit the sos_server.py file to update the email and Slack configuration:

Email Settings: Replace the placeholders with your email credentials and SMTP server information.

python
Copy code
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_SMTP_SERVER = "smtp.example.com"
EMAIL_SMTP_PORT = 587  # Use 587 for TLS
RECIPIENT_EMAIL = "recipient@example.com"
Slack Webhook: Replace SLACK_WEBHOOK_URL with your actual Slack Incoming Webhook URL.

python
Copy code
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/slack/webhook"
4. Running the Server
Start the Flask server:

bash
Copy code
python sos_server.py
The server will start on http://0.0.0.0:5000. It will listen for incoming SOS alerts from workstations and send notifications.

5. Deploy the SOS Button on Workstations
The SOS button application is designed for Windows workstations. To run it, follow these steps:

Install Python on the workstation.

Create an executable from the Python script using PyInstaller:

bash
Copy code
pyinstaller --onefile --windowed sos_button.py
Distribute the generated executable to workstations or package it as an MSI (see the packaging section below).

6. Packaging as an MSI Installer (Optional)
If you'd like to distribute the SOS button as an MSI installer, follow the steps in the documentation or use a tool like WiX Toolset or Inno Setup.

Server Endpoint
The SOS button sends a POST request to the /sos endpoint of the Flask server with the following JSON payload:

json
Copy code
{
  "message": "SOS triggered!",
  "ip_address": "192.168.x.x",
  "workstation_name": "DESKTOP-XYZ",
  "current_user": "username"
}
Response
The server will respond with the following JSON object, indicating the status of email and Slack notifications:

json
Copy code
{
  "status": "SOS notification received",
  "email_status": "Email sent successfully",
  "slack_status": "Slack notification sent successfully"
}
Customization
You can modify the behavior of the server by adding additional notification methods (e.g., SMS), or change the UI of the SOS button application to suit your needs.

Contributing
Fork the repository.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.
