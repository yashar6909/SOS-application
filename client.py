import tkinter as tk
import requests
import socket
import os
import time
import threading

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

def send_sos(num_alerts=3, delay_between_alerts=1):
    """
    Sends multiple SOS alerts with a delay between each.
    
    Args:
        num_alerts (int): Number of alerts to send.
        delay_between_alerts (int): Delay (in seconds) between alerts.
    """
    try:
        # Replace with your server endpoint
        server_url = "http://{serverURLhere}:5000/sos"
        
        # Get the workstation information
        workstation_info = get_workstation_info()
        
        if workstation_info:
            for i in range(num_alerts):
                # Send a POST request to the central server with workstation info
                response = requests.post(server_url, json={
                    "message": f"SOS triggered! Alert {i+1}",
                    "ip_address": workstation_info["ip_address"],
                    "workstation_name": workstation_info["workstation_name"],
                    "current_user": workstation_info["current_user"]
                })
                
                if response.status_code == 200:
                    print(f"SOS Alert {i+1} sent successfully")
                else:
                    print(f"Failed to send SOS Alert {i+1}: {response.status_code}")
                
                # Wait for the specified delay before sending the next alert
                if i < num_alerts - 1:
                    time.sleep(delay_between_alerts)
        else:
            print("Failed to collect workstation info.")
    except Exception as e:
        print(f"Error sending SOS: {e}")

def on_sos_click():
    """
    Starts a thread to send SOS alerts to avoid blocking the main GUI thread.
    """
    threading.Thread(target=send_sos, args=(3, 2)).start()  # Sends 3 alerts with 2 seconds delay between each

# Set up the GUI for SOS button
root = tk.Tk()
root.title("SOS Button")

# Make the window always on top and set no border
root.overrideredirect(True)  # Removes the window border
root.attributes("-topmost", True)  # Keep it on top of all windows

# Set the button appearance
sos_button = tk.Button(root, text="SOS", command=on_sos_click, font=("Arial", 20), bg="red", fg="white")
sos_button.pack(pady=20, padx=20)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the horizontal position (center of the screen)
window_width = 200  # Width of the SOS button window
x_position = (screen_width // 2) - (window_width // 2)

# Set the window position (top-middle of the screen)
root.geometry(f"{window_width}x100+{x_position}+0")  # Adjust window height and y-position as needed

root.mainloop()
