# SOS Alert System with AES Encryption (UDP Communication)

This project implements an SOS alert system where a client sends an emergency alert to a central server using **UDP** for communication. The alert is encrypted using **AES encryption** (via the Fernet module from the `cryptography` library) to ensure secure transmission of the alert data.

Once the server receives and decrypts the SOS alert, it sends notifications via **Slack Webhook** and **Email**.

## Features

- **UDP Communication**: Lightweight and fast communication between the client and server using UDP.
- **AES Encryption**: The SOS alerts are securely encrypted using AES encryption (Fernet) before transmission.
- **Slack Notification**: The server sends the alert details to a Slack channel via a webhook.
- **Email Notification**: The server sends the alert details via email using an SMTP server.
- **Responsive Client UI**: The client uses a **Tkinter** UI for the SOS button and doesn’t block the user interface during alert transmission.

## Requirements

- **Python 3.x**
- Python Libraries:
  - `cryptography` (for AES encryption/decryption)
  - `requests` (for sending Slack notifications)
  - SMTP server for sending emails

### Python Libraries Installation

To install the necessary Python libraries, run the following command:

```bash
pip install cryptography requests
```

## How It Works

1. The **client** collects workstation information (IP address, hostname, and logged-in user), encrypts the data using AES, and sends it over UDP to the server.
2. The **server** listens for incoming UDP packets, decrypts the data, and sends the alert details via Slack and email.

## Security Considerations

- **AES Encryption**: The SOS alerts are encrypted with a 32-byte AES key (using the Fernet module). This key must be securely shared between the client and server.
- **UDP Limitations**: Since UDP is connectionless and does not guarantee delivery, the client sends the SOS alert without confirmation of receipt. You may want to add retries or acknowledgments if needed.
- **Email and Slack Credentials**: Ensure that your email credentials and Slack Webhook URL are stored securely, possibly using environment variables.

## Setup Instructions

### 1. Server Setup

1. Clone this repository or copy the server code from this repository.
2. Install the required Python packages:
   ```bash
   pip install cryptography requests
   ```
3. Set up your email and Slack Webhook credentials in the server script:
   - **Email Setup**: Update the following variables in the server script with your email settings:
     ```python
     EMAIL_ADDRESS = "your_email@example.com"
     EMAIL_PASSWORD = "your_email_password"
     EMAIL_SMTP_SERVER = "smtp.example.com"  # For example: smtp.gmail.com
     EMAIL_SMTP_PORT = 587  # Use 587 for TLS
     RECIPIENT_EMAIL = "recipient@example.com"
     ```
   - **Slack Webhook Setup**: Replace the `SLACK_WEBHOOK_URL` variable with your Slack webhook URL:
     ```python
     SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/your/slack/webhook"
     ```

4. **Run the server**:
   ```bash
   python server.py
   ```
   The server will start listening on port `5000` for incoming UDP packets.

### 2. Client Setup

1. Clone this repository or copy the client code from this repository.
2. Install the required Python packages:
   ```bash
   pip install cryptography
   ```
3. Generate a 32-byte AES key that will be used by both the client and server:
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print(key.decode())  # Copy this key and use it in both client and server
   ```
4. Set this key in the client and server scripts:
   - In both the client and server scripts, update the `KEY` variable:
     ```python
     KEY = b'your_32_byte_secret_key_here'  # Replace with your generated key
     ```

5. **Run the client**:
   ```bash
   python client.py
   ```

6. The client provides a GUI SOS button. When clicked, it sends an encrypted SOS alert to the server via UDP.

## Communication Flow

1. **Client** sends an encrypted SOS message over UDP.
2. **Server** decrypts the message and sends notifications:
   - **Slack Webhook**: The server sends the alert details to a Slack channel via the configured webhook.
   - **Email**: The server sends an email with the alert details to the specified recipient.

## Example Slack and Email Notification

After receiving an SOS alert, the server will send notifications that look like this:

### Example Slack Message:
```
SOS Alert triggered!
Message: SOS triggered!
IP Address: 192.168.1.100
Workstation Name: DESKTOP-XYZ
Current User: user123
```

### Example Email Notification:
**Subject**: SOS Alert from Workstation

**Body**:
```
SOS Alert triggered!
Message: SOS triggered!
IP Address: 192.168.1.100
Workstation Name: DESKTOP-XYZ
Current User: user123
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute to this project! Here’s how:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a pull request.

## Contact

For any questions or issues, please feel free to create an issue in the GitHub repository or reach out at [yashar6909@gmail.com].

