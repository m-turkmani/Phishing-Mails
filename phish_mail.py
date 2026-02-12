#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import time
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Farben für die Konsole
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CLEAR = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def help_message():
    print(f"""
{Colors.YELLOW}--- Usage Instructions ---{Colors.CLEAR}

{Colors.BOLD}Preparation:{Colors.CLEAR}
1. Create a file {Colors.BLUE}message.html{Colors.CLEAR} containing your email content.
2. If you have multiple targets, create a {Colors.BLUE}targets.txt{Colors.CLEAR} file where each 
   email address is listed on a new line.

{Colors.BOLD}For your local relay (for testing):{Colors.CLEAR}
- Start your relay (e.g., {Colors.GREEN}aiosmtpd -n -l localhost:1025{Colors.CLEAR}).
- In the script, enter {Colors.YELLOW}localhost{Colors.CLEAR} as the host and {Colors.YELLOW}1025{Colors.CLEAR} as the port.
- Leave username and password empty.

{Colors.BOLD}For external SMTP servers (e.g., port 587):{Colors.CLEAR}
- Enter the provider's host.
- Enable STARTTLS (y).
- Enter your real credentials.

{Colors.RED}Delivery notice:{Colors.CLEAR} 
If you use a local relay without authentication, emails sent to external 
addresses (such as @gmail.com) will most likely be rejected because your computer 
is not an authorized mail server for the sender domain (SPF/DKIM validation). 
However, for internal pentests within a corporate network, the relay usually works 
very well if the internal gateway allows emails from pentest machines.
""")

def show_alert():
    clear()
    alert = f"""{Colors.RED}
                      /\\   | |         | |   | | | |
                     /  \\  | | ___ _ __| |_  | | | |
                    / /\\ \\ | |/ _ \\ '__| __| | | | |
                   / ____ \\| |  __/ |  | |_  |_| |_|
                  /_/    \\_\\_|\\___|_|   \\__| (_) (_)
                                   

    <><><><><><><><><><><><><><><ALERT!><><><><><><><><><><><><><><><>
    ! This tool is intended solely for educational and awareness     !
    ! purposes about the dangers of phishing. Using this tool in     !
    ! unauthorized environments or for malicious activities is       !
    ! strictly prohibited.                                           !
    <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
    !                                                                !     
    ! By running this tool, you agree to use it ethically and        !
    ! responsibly. We are not responsible for any misuse or illegal  ! 
    ! use of this tool. Be sure to obtain proper consent before      !
    ! conducting awareness tests.                                    ! 
    <><><><><><><><><><><><><><><ALERT!><><><><><><><><><><><><><><><>
    {Colors.CLEAR}"""
    print(alert)
    consent = input(f"{Colors.BLUE}Do you agree? ({Colors.GREEN}yes{Colors.BLUE} or {Colors.RED}no{Colors.BLUE})> {Colors.CLEAR}")
    
    if consent.lower() == 'yes':
        print(f"\n{Colors.GREEN}[+] I have permission and am authorized to perform this pentest.{Colors.CLEAR}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{Colors.RED}[!] Access Denied.{Colors.CLEAR}")
        sys.exit()

def banner():
    clear()
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print(r"""
 ____  _   _ ___ ____  _   _ _____ ____   __  __    _    ___ _     
|  _ \| | | |_ _/ ___|| | | | ____|  _ \ |  \/  |  / \  |_ _| |    
| |_) | |_| || |\___ \| |_| |  _| | | | || |\/| | / _ \  | || |    
|  __/|  _  || | ___) |  _  | |___| |_| || |  | |/ ___ \ | || |___ 
|_|   |_| |_|___|____/|_| |_|_____|____/ |_|  |_/_/   \_\___|_____|
    """)
    print(f"    --- SMTP Pentest & Relay Tool v1.0 ---")
    print(f"{Colors.RED}    --- Autor: Mohamad Turkmani ---{Colors.CLEAR}\n")

    print(f"""{Colors.RED}
[!] AUTHORIZED USE ONLY
    This tool is for approved security testing/training on systems you own
    or where you have explicit written permission.

    Misuse may be illegal and can lead to disciplinary/criminal consequences.
""")

def send_mail(smtp_config, victim, sender_email, subject, body_content):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = victim
        msg['Subject'] = subject
        msg.attach(MIMEText(body_content, 'html'))

        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'], timeout=10)
        
        if smtp_config['use_tls']:
            server.starttls()

        if smtp_config['user'] and smtp_config['pass']:
            server.login(smtp_config['user'], smtp_config['pass'])

        server.send_message(msg)
        server.quit()
        print(f"{Colors.GREEN}[+]{Colors.CLEAR} Success: Email sent to: {victim}")
        return True
    except Exception as e:
        print(f"{Colors.RED}[-]{Colors.CLEAR} Error with {victim}: {e}")
        return False

def main():
    show_alert()
    
    while True:
        banner()
        print(f"{Colors.YELLOW}--- MAIN MENU ---{Colors.CLEAR}")
        print("1) Phished Mail start ")
        print("3) Help ")
        print("99) exit ")
        
        try:
            choice = int(input(f"\n{Colors.BLUE}Choice> {Colors.CLEAR}"))
        except ValueError:
            continue

        if choice == 1:
            print(f"\n{Colors.YELLOW}--- SMTP Configuration ---{Colors.CLEAR}")
            
            host = input("Relay/SMTP Server (z.B. localhost oder mail.server.de): ").strip()
            
            # Prüfung ob Host leer ist
            if not host:
                print(f"{Colors.RED}[!] Error: You must enter a relay or an SMTP server.{Colors.CLEAR}")
                time.sleep(2)
                continue

            try:
                port_input = input("Port (z.B. 1025, 25, 587): ")
                if not port_input:
                    print(f"{Colors.RED}[!] Error: Port must not be empty.{Colors.CLEAR}")
                    time.sleep(2)
                    continue
                port = int(port_input)
            except ValueError:
                print(f"{Colors.RED}[!] Error: Invalid port (must be a number).{Colors.CLEAR}")
                time.sleep(2)
                continue
            
            use_tls = input("Use STARTTLS? (y/n): ").lower() == 'y'
            user = input("SMTP Login User (leave blank for anonymous relay): ")
            pw = input("SMTP Password (leave blank for anonymous relay): ")

            smtp_config = {'host': host, 'port': port, 'user': user, 'pass': pw, 'use_tls': use_tls}

            print(f"\n{Colors.YELLOW}--- E-Mail Details ---{Colors.CLEAR}")
            sender_display = input("Display name/Fake sender (e.g. IT-Support <it@firma.de>): ")
            subject = input("Subject: ")
            body_path = input("Path to the message file (e.g. mail.html): ")

            try:
                with open(body_path, 'r', encoding='utf-8') as f:
                    message_body = f.read()
            except FileNotFoundError:
                print(f"{Colors.RED}File not found.{Colors.CLEAR}")
                time.sleep(2)
                continue

            print(f"\n{Colors.YELLOW}--- Target Selection ---{Colors.CLEAR}")
            print("1) Single target address: ")
            print("2) Multiple targets from file: ")
            mode = input("> ")

            targets = []
            if mode == '1':
                targets.append(input("Recipient E-Mail: "))
            elif mode == '2':
                list_path = input("Path to email list (one email per line): ")
                try:
                    with open(list_path, 'r') as f:
                        targets = [line.strip() for line in f if "@" in line]
                except FileNotFoundError:
                    print(f"{Colors.RED}Error: Email list not found! {Colors.CLEAR}")
                    time.sleep(2)
                    continue
            else:
                print("Invalid selection. ")
                time.sleep(2)
                continue

            if not targets:
                print(f"{Colors.RED}No valid targets found. {Colors.CLEAR}")
                time.sleep(2)
                continue

            print(f"\n{Colors.BLUE}[*] Starting to send {len(targets)} E-Mails...{Colors.CLEAR}")
            count = 0
            for target in targets:
                if send_mail(smtp_config, target, sender_display, subject, message_body):
                    count += 1
                time.sleep(1)

            print(f"\n{Colors.GREEN}{Colors.BOLD}[*] Done! {count}/{len(targets)} Mails sent successfully.{Colors.CLEAR}")
            input("Press Enter to return to the main menu...")

        elif choice == 3: # Help
            while True:
                help_message()
                entry = input(f"{Colors.YELLOW}Go back to the Main Menu? (yes)> {Colors.CLEAR}")
                if entry.lower() == 'yes':
                    break

        elif choice == 99: # Exit
            print(f"""{Colors.CLEAR}
Leaving already? Aw, now you owe me a coffee! Help keep my coding sessions fueled
by donating. Thank youu! 

>> >> >> {Colors.YELLOW}https://www.paypal.com/paypalme/mohammadturkmani?country.x=DE&locale.x=de_DE{Colors.CLEAR} << << <<
""")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Cancelled by user.")
        sys.exit()
