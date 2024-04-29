import socket

host = "127.0.0.1"
port = 7777

def get_difficulty():
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty in ["easy", "medium", "hard"]:
            return difficulty
        else:
            print("Invalid difficulty. Please choose again.")

s = socket.socket()
s.connect((host, port))

# Receive the banner
data = s.recv(1024)
# Print banner
print(data.decode().strip())

while True:
    # Get user's name
    name = input("Enter your name: ").strip()
    s.sendall(name.encode())
    # Get difficulty level from user
    difficulty = get_difficulty()
    s.sendall(difficulty.encode())

    while True:
        user_input = input("").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        if "Correct" in reply:
            print(reply)
            break
        print(reply)
        continue
    
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again != "yes":
        break

s.close()
