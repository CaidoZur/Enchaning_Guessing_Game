import socket
import random
import json

host = "127.0.0.1"
port = 7777
banner = """
== Guessing Game v1.0 ==
Enter your guess:"""

# Function to generate a random integer based on difficulty level
def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 500)
    else:
        return random.randint(1, 100)  # Default to medium difficulty

# Function to load leaderboard data from file
def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard_data = json.load(file)
    except FileNotFoundError:
        leaderboard_data = []
    return leaderboard_data

# Function to update leaderboard data and save to file
def update_leaderboard(name, score):
    leaderboard_data = load_leaderboard()
    leaderboard_data.append({"name": name, "score": score})
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard_data, file)

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"Server is listening on port {port}")

conn = None
while True:
    if conn is None:
        print("Waiting for connection..")
        conn, addr = s.accept()
        print(f"New client connected: {addr[0]}")
    else:
        guessme = generate_random_int("medium")  # Default to medium difficulty
        conn.sendall(banner.encode())
        attempts = 0
        while True:
            client_input = conn.recv(1024)
            guess = int(client_input.decode().strip())
            print(f"User guess attempt: {guess}")
            attempts += 1
            if guess == guessme:
                conn.sendall(b"Correct Answer!\n")
                name = conn.recv(1024).decode().strip()
                update_leaderboard(name, attempts)
                break
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nEnter guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nEnter guess: ")
        conn.sendall(b"Thank you for playing!\n")
        conn.close()
        conn = None
