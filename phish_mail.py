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
    CYAN = '\033[96m' # Nachgetragen, da im Original in show_alert verwendet
    CLEAR = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def help_message():
    print(f"""
{Colors.YELLOW}--- Usage Instructions & Technical Overview ---{Colors.CLEAR}

{Colors.BOLD}1. Preparation:{Colors.CLEAR}
- Create {Colors.BLUE}message.html{Colors.CLEAR} with your HTML phishing template.
- Create {Colors.BLUE}targets.txt{Colors.CLEAR} (one email per line) for mass delivery.

{Colors.BOLD}2. Local Testing Mode (The "Safety Lab"):{Colors.CLEAR}
- {Colors.CYAN}How it works:{Colors.CLEAR} You use a local sink like {Colors.GREEN}aiosmtpd{Colors.CLEAR} or your {Colors.GREEN}fake_smtp.py{Colors.CLEAR}.
- {Colors.CYAN}Function:{Colors.CLEAR} These tools act as "Blackhole" servers. They accept the SMTP 
  connection from this script but do NOT forward the mail to the internet.
- {Colors.CYAN}Setup:{Colors.CLEAR} 
  1. Start: {Colors.YELLOW}python3 fake_smtp.py{Colors.CLEAR}
  2. In this script: Host={Colors.YELLOW}localhost{Colors.CLEAR}, Port={Colors.YELLOW}1025/1026{Colors.CLEAR}, No Auth/TLS.
- {Colors.CYAN}Benefit:{Colors.CLEAR} Perfect for checking if your HTML layout and the "Fake Sender" 
  display name look correct without triggering any real mail filters.

{Colors.BOLD}3. Real Production Mode (The "Engagement"):{Colors.CLEAR}
- {Colors.CYAN}How it works:{Colors.CLEAR} This script connects directly to a real Mail Transfer Agent (MTA).
- {Colors.CYAN}Setup:{Colors.CLEAR} Use hosts like {Colors.YELLOW}smtp.gmail.com{Colors.CLEAR} or {Colors.YELLOW}smtp.sendgrid.net{Colors.CLEAR}.
- {Colors.CYAN}Requirements:{Colors.CLEAR} Port 587, STARTTLS={Colors.YELLOW}y{Colors.CLEAR}, and valid credentials.

{Colors.RED}Important Delivery Notice:{Colors.CLEAR}
A local relay (fake_smtp) cannot send to real addresses (like @gmail.com) 
because it lacks SPF/DKIM signatures and a fixed IP. For real-world 
delivery, always use a verified SMTP provider or an authorized internal 
company relay that trusts your IP.
""")

def show_alert():
    clear()
    alert = f"""
    {Colors.RED}{Colors.BOLD}┌──────────────────────────────────────────────────────────────────────────┐
    │                            LEGAL DISCLAIMER                              │
    ├──────────────────────────────────────────────────────────────────────────┤
    │                                                                          │
    │  {Colors.YELLOW}WARNING:{Colors.RED} This tool is for EDUCATIONAL and AUTHORIZED testing only.      │
    │                                                                          │
    │  1. Unauthorized use of this tool is strictly prohibited.                │
    │  2. You must have explicit written consent from the target.              │
    │  3. The author is NOT responsible for any misuse or legal actions.       │
    │                                                                          │
    │  By continuing, you confirm you are acting as an ethical professional.   │
    │                                                                          │
    └──────────────────────────────────────────────────────────────────────────┘{Colors.CLEAR}
    """
    print(alert)
    consent = input(f"    {Colors.CYAN}Do you agree to these terms? ({Colors.GREEN}yes{Colors.CYAN}/{Colors.RED}no{Colors.CYAN})> {Colors.CLEAR}")
    
    if consent.lower() == 'yes':
        print(f"\n    {Colors.GREEN}[✓] Authorization confirmed. Initializing core modules...{Colors.CLEAR}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n    {Colors.RED}[!] Session terminated. Access Denied.{Colors.CLEAR}")
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
            choice_input = input(f"\n{Colors.BLUE}Choice> {Colors.CLEAR}")
            if not choice_input: continue
            choice = int(choice_input)
        except ValueError:
            continue

        if choice == 1:
            print(f"\n{Colors.YELLOW}--- SMTP Configuration ---{Colors.CLEAR}")
            
            host = input("Relay/SMTP Server (z.B. localhost oder mail.server.de): ").strip()
            
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
                    with open(list_path, 'r', encoding='utf-8') as f:
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

        elif choice == 3:
            while True:
                help_message()
                entry = input(f"{Colors.YELLOW}Go back to the Main Menu? (yes)> {Colors.CLEAR}")
                if entry.lower() == 'yes':
                    break

        elif choice == 99:
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
