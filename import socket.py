import socket
import threading

HOST = '192.168.1.62'
PORT = 5000

conn = None

def listen_for_data():
    global conn
    while True:
        data = conn.recv(1024)
        if not data:
            print("ESP32 disconnected.")
            break
        print("Received:", data.decode().strip())

def listen_for_input():
    global conn
    while True:
        cmd = input("Type 'q' to close connection: ").strip()
        if cmd.lower() == 'q':
            try:
                conn.sendall(b"CLOSE\n")
                print("Sent CLOSE command to ESP32.")
                conn.close()
            except:
                pass
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    # Start threads
    threading.Thread(target=listen_for_data, daemon=True).start()
    listen_for_input()