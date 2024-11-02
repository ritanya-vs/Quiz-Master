import socket
import threading
import sys
import random

# Setup server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check for proper usage
if len(sys.argv) != 3:
    print("Usage: python server.py <IP Address> <Port Number>")
    sys.exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# Bind and listen for incoming connections
server.bind((IP_address, Port))
server.listen(100)

list_of_clients = []
questions = [
    "What is the Italian word for PIE? \n a. Mozarella b. Pasty c. Patty d. Pizza",
    "Water boils at 212 Units at which scale? \n a. Fahrenheit b. Celsius c. Rankine d. Kelvin",
    "Which sea creature has three hearts? \n a. Dolphin b. Octopus c. Walrus d. Seal",
    "What is the capital of France? \n a. London b. Berlin c. Paris d. Madrid",
    "Which planet is known as the Red Planet? \n a. Earth b. Mars c. Jupiter d. Venus",
    "What is the largest mammal in the world? \n a. Elephant b. Blue Whale c. Giraffe d. Hippo",
    "Which element has the chemical symbol 'O'? \n a. Gold b. Oxygen c. Osmium d. Oganesson",
    "What is the tallest mountain in the world? \n a. K2 b. Kangchenjunga c. Mount Everest d. Lhotse",
    "Who wrote 'Romeo and Juliet'? \n a. Mark Twain b. Charles Dickens c. William Shakespeare d. J.K. Rowling",
    "What is the hardest natural substance on Earth? \n a. Gold b. Iron c. Diamond d. Quartz",
]
answers = ['d', 'a', 'b', 'c', 'b', 'b', 'b', 'c', 'c', 'c']  # Correct answers
client_scores = {}  # Track each client's score
buzz_lock = threading.Lock()
buzzed_client = None
curr_qind = -1

# Broadcast message to all connected clients
def broadcast(message):
    for client in list_of_clients:
        try:
            client.send(message.encode())
        except:
            client.close()
            remove(client)

# Handle individual client connections
def clientthread(conn, addr):
    global buzzed_client, curr_qind
    conn.send(b"Welcome to the quiz! First to 5 correct answers wins.\nPress Enter to buzz in for each question.\n")
    client_scores[conn] = 0

    while True:
        try:
            # Wait for the client to press Enter to buzz in
            message = conn.recv(2048).decode().strip()
            if not message:
                continue  # Ignore empty messages, keep waiting for buzz

            with buzz_lock:
                if buzzed_client is None:
                    # This client buzzed first
                    buzzed_client = conn
                    curr_qind = random.randint(0, len(questions) - 1)
                    question = questions[curr_qind]
                    conn.send(f"You buzzed in first! Here is your question:\n{question}".encode())
                    broadcast(f"Player {list_of_clients.index(conn) + 1} buzzed in and is answering.\n")
                elif conn == buzzed_client:
                    # Process the answer if it's from the buzzed client
                    answer = message.strip().lower()
                    if answer in ['a', 'b', 'c', 'd']:
                        process_answer(conn, answer)  # Process answer
                        reset_buzzer()  # Reset buzzer for the next question
                    else:
                        conn.send(b"Invalid answer. Please respond with a, b, c, or d.\n")
                else:
                    conn.send(b"Another player buzzed first. Wait for the next question.\n")
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break  

    remove(conn)

# Process client's answer and update score
def process_answer(conn, answer):
    global curr_qind

    if answer == answers[curr_qind]:
        client_scores[conn] += 1
        broadcast(f"Correct! Player {list_of_clients.index(conn) + 1} scores a point.\n")
        
        # Check if this player has won by reaching 5 points
        if client_scores[conn] >= 5:
            broadcast(f"Player {list_of_clients.index(conn) + 1} wins with 5 points!\n")
            end_quiz()  # End the game when a player reaches 5 points
            return
    else:
        client_scores[conn] -= 1
        broadcast(f"Incorrect! Player {list_of_clients.index(conn) + 1} loses a point.\n")

    # Show scores after each question
    show_scores()

    # Remove the used question and answer
    questions.pop(curr_qind)
    answers.pop(curr_qind)

    # End the quiz if there are no more questions left
    if len(questions) == 0:
        end_quiz()
    else:
        reset_buzzer()  


# Show current scores to all clients
def show_scores():
    scores_message = "Current Scores:\n"
    for idx, conn in enumerate(list_of_clients):
        scores_message += f"Player {idx + 1}: {client_scores[conn]} points\n"
    broadcast(scores_message)

# Reset buzzer for next question
def reset_buzzer():
    global buzzed_client
    buzzed_client = None
    if questions:
        broadcast("Prepare to buzz for the next question...\n")

# Remove a client from the client list
def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)
        del client_scores[conn]

# End the quiz and display final scores
def end_quiz():
    broadcast("Game Over\n")
    for i, conn in enumerate(list_of_clients):
        conn.send(f"You scored {client_scores[conn]} points.".encode())
    server.close()
    sys.exit()

# Accept new client connections
def accept_clients():
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(f"{addr[0]} connected")
        threading.Thread(target=clientthread, args=(conn, addr)).start()

accept_clients()