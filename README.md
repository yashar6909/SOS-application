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

