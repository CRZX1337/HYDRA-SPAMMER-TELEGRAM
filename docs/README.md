HYDRA SPAMMER - Quick Start Guide

WARNING: This tool is for testing and educational purposes ONLY.
Spamming is against Telegram's rules and can get your accounts banned.
Use RESPONSIBLY and at your OWN RISK.

What is Hydra Spammer?

Hydra Spammer uses multiple Telegram accounts to send spam messages concurrently.

Setup:

1. Get API Keys:
   - Go to https://my.telegram.org/apps and get your API ID and API Hash.

2. Edit accounts.txt:
   - Open `accounts.txt` and enter your account details in this format (one account per line):
     API_ID,API_HASH,PHONE_NUMBER
   - Example:
     1234567,YOUR_API_HASH,+1234567890
     8765432,ANOTHER_API_HASH,+9876543210
   - **IMPORTANT:** You need to authorize each phone number with Telegram API at least once.

3. Install Libraries:
   - Make sure you have Python installed (3.7 or higher).
   - Run this command in your terminal to install required libraries:
     `pip install telethon python-dotenv`

How to Use:

1. Run the script:
   - Open a terminal in the same folder as `tgspammer.py` and run:
     `python tgspammer.py`

2. Follow Prompts:
   - The script will ask you questions:
     - Message type (single, multiple, random, dynamic)
     - Speed (normal or max - max speed = ban risk!)
     - Target username or phone number
     - Number of messages to send

3. Authorize Accounts:
   - If it's the first time using an account, you'll be asked for authorization codes and maybe 2FA passwords for each account.

Important Notes:

* BAN RISK: Max speed spamming is very risky and will likely get your accounts banned. Use normal speed or disposable accounts.
* accounts.txt:  Keep your `accounts.txt` file safe and don't share it.
* phrases.txt:  Create `phrases.txt` to use dynamic spam messages (one phrase per line).

Disclaimer:

This tool is for testing and educational purposes only. I am not responsible for how you use it. Be ethical and responsible.  Use at your own risk!
