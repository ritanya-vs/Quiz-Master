import socket
import threading
import sys

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure correct number of arguments are passed
if len(sys.argv) != 3:
    print("Usage: python client.py <IP Address> <Port>")
    sys.exit()

# Assign IP and Port from command line arguments
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Connect to the server
client_socket.connect((IP_address, Port))
print(f"Connected to server at {IP_address}:{Port}")

# Function to listen for messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if not message:
                print("Disconnected from server")
                client_socket.close()
                break

            print(message)

            # Check for "Game Over" message to stop the client
            if "Game Over" in message:
                print("Thank you for playing!")
                client_socket.close()
                break

        except Exception as e:
            print("An error occurred:", e)
            client_socket.close()
            break


# Start a thread to listen for server messages
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    try:
        # Buzz in by pressing Enter
        input("Press Enter to buzz in: ")
        client_socket.send(b"BUZZER")

        # Allow user to answer if prompted by the server
        response = input("Enter your answer (a, b, c, or d): ").strip().lower()
        if response in ['a', 'b', 'c', 'd']:
            client_socket.send(response.encode())
        else:
            print("Invalid response. Please use a, b, c, or d.")

    except KeyboardInterrupt:
        print("\nExiting...")
        client_socket.close()
        sys.exit()
    except Exception as e:
        print("An error occurred:", e)
        client_socket.close()
        sys.exit() 