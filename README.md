# studentproductivity





import socket
import threading

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

clients = {}
lock = threading.Lock()

def handle_client(client, addr):
    try:
        username = client.recv(1024).decode()
        with lock:
            if username in clients:
                client.send("Username already taken!".encode())
                client.close()
                return
            clients[username] = client
            print(f"{username} joined from {addr}")

        # Notify all users
        broadcast(f"{username} has joined the chat!", "Server")

        while True:
            msg = client.recv(1024).decode()
            if not msg or msg.lower() == "exit":
                break
            broadcast(msg, username)
        
    except:
        pass
    finally:
        with lock:
            del clients[username]
        print(f"{username} left the chat")
        broadcast(f"{username} has left the chat", "Server")
        client.close()

def broadcast(msg, sender):
    with lock:
        for user, conn in clients.items():
            try:
                conn.send(f"{sender}: {msg}".encode())
            except:
                conn.close()
                del clients[user]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()









import socket
import threading

SERVER_IP = "127.0.0.1"  # Change this if running on LAN
SERVER_PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    username = input("Enter a unique username: ")
    client.send(username.encode())

    server_response = client.recv(1024).decode()
    if server_response == "Username already taken!":
        print("This username is already in use. Try another one.")
        client.close()
        return

    print("Connected! Type messages or 'exit' to leave.")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        client.send(msg.encode())

    client.close()

if __name__ == "__main__":
    start_client()

