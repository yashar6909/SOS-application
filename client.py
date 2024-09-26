import socket
import os
import threading
from cryptography.fernet import Fernet

# AES Encryption Key (Must be the same as the one on the server)
KEY = b'your_32_byte_secret_key_here'  # Ensure this key is 32 bytes

# Initialize Fernet with the AES key
cipher_suite = Fernet(KEY)

def get_workstation_info():
    try:
        # Get the IP address of the workstation
        ip_address = socket.gethostbyname(socket.gethostname())
        
        # Get the name of the workstation (hostname)
        workstation_name = socket.gethostname()
        
        # Get the name of the currently logged-in user
        current_user = os.getlogin()
        
        return {
            "ip_address": ip_address,
            "workstation_name": workstation_name,
            "current_user": current_user
        }
    except Exception as e:
        print(f"Error fetching workstation info: {e}")
        return None

def encrypt_data(data):
    """
    Encrypt the given data using AES (Fernet) encryption.
    """
    # Convert dictionary to string, then bytes
    data_bytes = str(data).encode('utf-8')
    # Encrypt the data
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data

def send_sos():
    """
    Sends a single SOS alert via UDP socket without blocking the UI.
    """
    try:
        # Replace with your server IP and port (where UDP server is listening)
        server_ip = "127.0.0.1"  # Localhost for testing
        server_port = 5000

        # Get the workstation information
        workstation_info = get_workstation_info()

        if workstation_info:
            # Prepare the message
            workstation_info["message"] = "SOS triggered!"
            
            # Encrypt the payload
            encrypted_payload = encrypt_data(workstation_info)
            
            # Create a UDP socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                # Send the encrypted data to the server
                sock.sendto(encrypted_payload, (server_ip, server_port))
                print("SOS Alert sent successfully via UDP.")
        else:
            print("Failed to collect workstation info.")
    except Exception as e:
        print(f"Error sending SOS: {e}")

def on_sos_click():
    """
    Starts a thread to send a single SOS alert to avoid blocking the main GUI thread.
    """
    threading.Thread(target=send_sos).start()  # Send 1 alert in a separate thread

# Tkinter GUI code for SOS button remains unchanged
import tkinter as tk
root = tk.Tk()
root.title("SOS Button")
root.overrideredirect(True)
root.attributes("-topmost", True)
sos_button = tk.Button(root, text="SOS", command=on_sos_click, font=("Arial", 20), bg="red", fg="white")
sos_button.pack(pady=20, padx=20)
screen_width = root.winfo_screenwidth()
window_width = 200
x_position = (screen_width // 2) - (window_width // 2)
root.geometry(f"{window_width}x100+{x_position}+0")
root.mainloop()
