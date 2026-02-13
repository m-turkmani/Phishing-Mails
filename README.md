# SMTP Pentest & Relay Tool (PHISHED MAIL)

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight Python tool designed for security professionals and penetration testers to conduct email phishing simulations and SMTP relay testing. This tool supports local test relays (unauthenticated) as well as external SMTP servers with STARTTLS and authentication.

## ⚠️ Disclaimer

**This tool is intended for educational purposes and authorized security testing only.**
Using this tool for malicious activities or without explicit written consent from the target organization is strictly prohibited. The author assumes no liability for any misuse or damage caused by this program. **Use at your own risk.**

---

## 🚀 Features

- **Flexible SMTP Configuration:** Quickly set up host, port, and TLS settings.
- **Anonymous Relay Support:** Test for open relays or use local testing environments (e.g., `aiosmtpd`).
- **HTML Payloads:** Send professional-looking phishing templates via `.html` files.
- **Bulk Delivery:** Import multiple target addresses from a text file (`targets.txt`).
- **Sender Spoofing:** Test email gateway filters by customizing the "Display Name" and "From" address.
- **Interactive CLI:** User-friendly menu and step-by-step configuration.

## 📋 Prerequisites

- **Python 3.x**
- No external libraries required (uses standard libraries like `smtplib` and `email`).

## 🛠 Setup & Preparation

1. **Clone the Repository:**
   ```bash
   apt update && apt upgrade
   apt install git -y
   git clone https://github.com/m-turkmani/Phishing-Mails.git
   cd Phished_Mail
   chmod +x phish_mail.py

<img width="643" height="253" alt="alert" src="https://github.com/user-attachments/assets/87ec4a5c-111b-4cff-9845-7a7f444b712a" />
<img width="564" height="372" alt="Image" src="https://github.com/user-attachments/assets/de631c9b-b569-4e1b-96e9-f2e67cfc3a9e" />


**2. Prepare your files:**
Create a file named message.html containing your email body.
(Optional) Create a targets.txt file with one email address per line.

📖 Usage
Run the script using Python:
```
python3 phish_mail.py

or

./phish_mail.py
```


Local Testing (Example)
To test the script safely without sending actual emails to the internet, you can run a local SMTP dummy server:

```
pip install aiosmtpd
or
apt install python3-aiosmtpd
python3 -m aiosmtpd -n -l localhost:1025

```
**2. Option B: Using the fake_smtp.py script**
If you prefer a more formatted output with clear labels for "Sender", "Recipient", and "Content", run the provided debugging script:
```
python3 fake_smtp.py
```
In the main script (phish_mail.py), use the following settings for local tests:

Host: localhost
Port: 1025 (or 1026 depending on your script config)
TLS/Authentication: Disabled (n)


**In the script, use localhost as the host and 1025 as the port, with TLS and Authentication disabled.**

**🛡 Security Controls**
Consent Gate: The script requires an explicit "yes" to confirm authorization before proceeding to the main menu.
TLS Support: Ensures compatibility with modern secure mail providers.

**☕ Support**
If this tool helped you in your security assessments, feel free to support the development! [PayPal Link included in the script]

**Author: Mohamad Turkmani**
Version: 1.0
Status: Stable / Optimized for internal pentesting.
