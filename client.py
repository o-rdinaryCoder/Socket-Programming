import socket

def play_game():
    """Function to play the jumbled word game."""
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8080))

    while True:
        # Receive the server's prompt
        prompt = client_socket.recv(1024).decode().strip()
        print(prompt)

        # Check if the prompt is about playing again or a jumbled word question
        if "Do you want to play again?" in prompt:
            play_again = input()
            client_socket.send(str.encode(play_again.lower()))
            if play_again.lower() != "yes":
                break
        else:
            # Prompt the user to unscramble the word and send the answer to the server
            answer = input("Enter your answer: ")
            client_socket.send(str.encode(answer))

            # Receive and print the server's response
            response = client_socket.recv(1024).decode()
            print(response)

    # Close the client socket
    client_socket.close()

# Call the play_game function to start playing
play_game()
