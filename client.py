import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = socket.gethostbyname(socket.gethostname())
    client.connect((ip_address, 9999))

    while True:
        response = ""
        while True:
            chunk = client.recv(1024).decode()
            if not chunk:
                print("Connection closed by server.")
                client.close()
                return
            response += chunk
            # check if we have received at least two newlines
            if response.count('\n') >= 2:
                break
        
        # split the response into lines
        lines = response.split('\n')
        if len(lines) < 3:
            print("Received malformed response.")
            continue
        
        try:
            status_code = int(lines[0].strip())
            status_phrase = lines[1].strip()  
            message = '\n'.join(lines[2:]).strip()
        except ValueError:
            print("Error parsing response.")
            continue

        print(f"Status code: {status_code}\nStatus phrase: {status_phrase}")
        print(message)

        if status_code == 410:  # game finished
            break

        guess = input("\nEnter your guess (1-500): ")
        client.send(guess.encode())

    client.close()

if __name__ == "__main__":
    main()