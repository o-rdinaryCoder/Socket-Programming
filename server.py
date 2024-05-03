import socket
import random

# List of jumbled words and their corresponding solutions
words = {
    "jgunle": "jungle",
    "obk": "book",
    "lyogolo": "oology",
    "nypthon": "python",
    "eveunen": "uneven"
}

def jumble_word(word):
    """Jumbles the letters of a word."""
    jumbled = list(word)
    random.shuffle(jumbled)
    return ''.join(jumbled)

def handle_client(conn, addr):
    """Handles communication with a client."""
    print(f"Client connected from {addr}")

    while True:
        # Select a random word from the list
        word = random.choice(list(words.keys()))
        jumbled_word = jumble_word(word)

        # Send the jumbled word to the client
        conn.send(str.encode(f"Unscramble the word: {jumbled_word}\n"))

        # Receive the client's answer
        answer = conn.recv(1024).decode().strip()

        # Check if the answer is correct
        if answer.lower() == words[word].lower():
            conn.send(str.encode("Congratulations! You unscrambled the word correctly.\n"))
        else:
            conn.send(str.encode(f"Sorry, the correct answer is '{words[word]}'\n"))

        # Ask the client if they want to play again
        conn.send(str.encode("Do you want to play again? (yes/no): "))
        
        try:
            play_again = conn.recv(1024).decode().strip().lower()
        except ConnectionResetError:
            print("Client closed the connection.")
            break

        if play_again != "yes":
            print("Client chose to stop playing.")
            break
        else:
            print("Client wants to play again.")

    print(f"Client disconnected from {addr}")
    conn.close()

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8080))
server_socket.listen(1)

print("Waiting for clients to connect...")

# Server loop to accept multiple client connections
while True:
    try:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        break

# Close the server socket
server_socket.close()
