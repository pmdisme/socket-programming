import socket
import random

# define status codes and phrases
STATUS_CODES = {
    200: "OK",
    400: "Bad Request",
    410: "Game Finished"
}

def get_status_phrase(code):
    return STATUS_CODES.get(code, "Unknown Status")

def play_game(client):
    answer = random.randint(1, 500)
    print("Number to guess:", answer)
    max_turns = 8
    turns_left = max_turns

    # message to the client
    initial_message = (
        f"{200}\n{get_status_phrase(200)}\n"
        f"Welcome to Guess The Number Game!\n"
        f"Guess a number between 1 and 500. You have {max_turns} turns.\n"
    )
    client.sendall(initial_message.encode())

    while turns_left > 0:
        try:
            guess = int(client.recv(1024).decode())
        except ValueError:
            error_message = (
                f"{400}\n{get_status_phrase(400)}\n"
                f"Please enter a valid number.\n"
            )
            client.sendall(error_message.encode())
            continue

        if guess < 1 or guess > 500:
            error_message = (
                f"{400}\n{get_status_phrase(400)}\n"
                f"Please enter a number in the range 1-500.\n"
            )
            client.sendall(error_message.encode())
        elif guess < answer:
            turns_left -= 1
            if turns_left == 0:
                response_message = (
                    f"{410}\n{get_status_phrase(410)}\n"
                    f"Game over! You've used all of your turns.\n"
                    f"The number was {answer}.\n"
                )
                client.sendall(response_message.encode())
                break
            else:
                response_message = (
                    f"{200}\n{get_status_phrase(200)}\n"
                    f"Too low! Try again.\n"
                    f"You have {turns_left} turns left.\n"
                )
                client.sendall(response_message.encode())
        elif guess > answer:
            turns_left -= 1
            if turns_left == 0:
                response_message = (
                    f"{410}\n{get_status_phrase(410)}\n"
                    f"Game over! You've used all of your turns.\n"
                    f"The number was {answer}.\n"
                )
                client.sendall(response_message.encode())
                break
            else:
                response_message = (
                    f"{200}\n{get_status_phrase(200)}\n"
                    f"Too high! Try again.\n"
                    f"You have {turns_left} turns left.\n"
                )
                client.sendall(response_message.encode())
        else:
            response_message = (
                f"{410}\n{get_status_phrase(410)}\n"
                f"Congratulations! You guessed it right.\n"
                f"The number was {answer}.\n"
            )
            client.sendall(response_message.encode())
            break
    
    client.close()

def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, 9999))
    server.listen(1)
    print("Server is waiting for clients...")

    while True:
        client, addr = server.accept()
        print(f"Connected to {addr}")
        play_game(client)
    
if __name__ == "__main__":
    main()