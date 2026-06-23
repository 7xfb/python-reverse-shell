import socket

with socket.socket() as s:
    port = 2002
    s.bind(('0.0.0.0', port))
    s.listen()
    print('[INFO] WAITING FOR CONNECTION...')
    conn, addr = s.accept()
    print(f'[NEW CLIENT] CONNECTED TO: {addr[0]}')

    while True:
        try:
            command = input("Command to send >> ")
            if not command:
                continue

            conn.send(command.encode())
        
            if command.lower() == "exit":
                break

            result = conn.recv(4096).decode()
            if not result:
                print("[NO OUTPUT]")
            print(result)
        
        except KeyboardInterrupt:
            print("\n[DISCONNECTED]")
            break
        except socket.error as e:
            print(f"[ERROR]: {e}")
            continue


    