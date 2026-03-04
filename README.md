# CAPTCHApocalypse-THM-BruteForce

`CAPTCHApocalypse-THM-BruteForce` is a tool designed for **TryHackMe students** trying to complete the [CAPTCHApocalypse room](https://tryhackme.com/room/captchapocalypse) room on TryHackMe.  

It automates brute‑force login attempts against CAPTCHA‑protected forms using **Selenium** and **Tesseract OCR**, providing a hands‑on example of combining browser automation with OCR to overcome CAPTCHA challenges in web exploitation.

This project was inspired and developed with knowledge gained from the [Tooling via Browser Automation room](https://tryhackme.com/room/customtoolingviabrowserautomation), which introduces the fundamentals of building custom tools with Selenium, and those concepts have been applied here to build a functional brute‑force tool for the CAPTCHApocalypse challenge.

---

## Room Information
- **Room Name:** CAPTCHApocalypse  
- **Room URL:** [https://tryhackme.com/room/captchapocalypse](https://tryhackme.com/room/captchapocalypse)

---

## Wordlist Preparation
This tool uses a shortened password list (`newrockyou.txt`) for faster testing.  
It was created by extracting the first 100 passwords from the original `rockyou.txt` wordlist.  
This ensures the brute‑force attempts run quickly while still demonstrating the attack.

```bash
head -n 100 /usr/share/wordlists/rockyou.txt > newrockyou.txt
```

---

## Requirements
All dependencies are listed in `requirements.txt`:

```txt
selenium
selenium-stealth
fake-useragent
pytesseract
Pillow
```

You can install them in one step:

```bash
pip install -r requirements.txt
```

---

## Usage
1. Clone or download this repository.
2. Place your `newrockyou.txt` wordlist in the project directory.
3. Edit the script configuration in **script.py** to add your target machine IP:
   ```python
   # CONFIG
   ip = 'http://TARGET_MACHINE_IP'
   login_url = f'{ip}/index.php'
   dashboard_url = f'{ip}/dashboard.php'
   username = "admin"
   ```

4. Run the script:
   ```bash
   python3 script.py
   ```
5. The output will show each attempt in a clear one‑line format:
   ```
   Password: abc123 | Captcha: 48UCD | Status: FAILED
   Password: secret123 | Captcha: X9KLM | Status: SUCCESS
   [+] FLAG{example_flag_here}
   ```

---

## Solving the Room
This tool can be used to solve the CAPTCHApocalypse room on TryHackMe.  
A full step‑by‑step write‑up is available in my blog post:  [CAPTCHApocalypse [TryHackMe] [Writeup]](https://aredopseagle.wordpress.com/2026/03/04/captchapocalypse-tryhackme-writeup/)


---

## Disclaimer
This project is for **educational purposes only**.  
Do not use it against systems you do not own or have explicit permission to test. Unauthorized use may violate laws and terms of service. The author assumes no responsibility for misuse.

---

## License
This project is licensed under the **MIT License** — meaning anyone can use, modify, and share it freely for learning and educational purposes.
