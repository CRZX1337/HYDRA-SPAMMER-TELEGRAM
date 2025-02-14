# <div align="center"> 😈 HYDRA-SPAMMER: Digital Torment Unleashed 😈 </div>
<p align="center">

</p>
<br>

<div align="center">
    <h3> Unleash a Torrent of Digital… <ins>Annoyance</ins> upon Unsuspecting Telegram Users </h3>
</div>

<p align="center">
    HYDRA-SPAMMER is a Python-based Telegram spamming instrument designed for <ins> "stress testing," </ins> <ins> "educational purposes," </ins> and other activities involving the <ins> repetitive dissemination of digital messages. </ins> (The <ins> irony </ins> drips, does it not?)
</p>

<hr>

## 📸 Preview Screenshots:  *Visual Distractions for the Simple-Minded*

<div align="center">
    <img src="https://github.com/CRZX1337/HYDRA-SPAMMER-TELEGRAM/blob/main/preview1.png" width="400" alt="Hydra-Spammer Preview Screenshot 1">
    <br>
    <br>
    <img src="https://github.com/CRZX1337/HYDRA-SPAMMER-TELEGRAM/blob/main/preview2.png" width="400" alt="Hydra-Spammer Preview Screenshot 2">
</div>

<hr>

## ⚙️ Key Features: Instruments of Minor Irritation

This script provides tools for generating digital discomfort:

*   **🎭 Versatile Message Types:**
    *   **Single Custom Message:** Deploy the same monotonous phrase repeatedly.
    *   **Multiple Custom Messages:** Cycle through a list of pre-scripted messages.
    *   **🎲 Random Message Generation:** Flood targets with nonsensical gibberish of adjustable length.

*   **⏱️ Adjustable Speed Modes:** Regulate the message flow:
    *   **🐢 Normal Speed (Default):**  A slower message stream to minimize detection.
    *   **🚀 Maximum Speed (⚠️ WARNING: BAN RISK ⚠️):** Unleash a rapid message flood, potentially leading to account limitations. Use with caution or disposable accounts.

*   **✨ Animated User Interface:** Includes loading animations and progress bars for visual feedback and to enhance user experience.
    *   Animation delays are configurable for slight adjustments.

*   **🛡️ Error Handling:** Basic error handling for common Telegram API issues (FloodWait, UserBlocked, etc.) is implemented to improve script robustness.

<hr>

## 🛠️ Installation: Assembling Your Toy

Prepare your environment for running the script:

1.  **🐍 Python:** Ensure you have Python 3.7 or higher installed. Verify with: `python3 --version` or `python --version`.

2.  **📦 pip:** Confirm `pip` (Python package installer) is installed.

3.  **📚 Libraries:** Install necessary Python libraries using `pip`:

    ```bash
    pip install telethon python-dotenv
    ```
    *   `telethon`: The Telegram API client.
    *   `python-dotenv`: For loading API keys from a `.env` file.

<hr>

## ⚙️ Configuration: Setting the Stage

1.  **🔑 Telegram API Keys:**  Acquire API access credentials from Telegram: [https://my.telegram.org/apps](https://my.telegram.org/apps). Obtain your `API ID` and `API Hash`.

2.  **📝 Create `.env` file:**  In the root directory of `hydra-spammer`, create a file named `.env`.

3.  **✍️ Populate `.env`:** Edit `.env` with your API credentials and phone number, referencing the ` .env.example` template. **Keep this file secure.**

    ```
    API_ID=YOUR_API_ID_HERE
    API_HASH=YOUR_API_HASH_HERE
    PHONE_NUMBER=+1234567890 # Example: US number
    NORMAL_SPEED_DELAY=0.5   # Optional: Adjust delay
    # USERNAME=YourUsername    # Optional: Cosmetic fluff
    ```

<hr>

## 🚀 Quick Start: Dive In

1.  **Clone:** Clone this repository: `git clone [repository URL - *you handle this triviality* ]`
2.  **Configure:** Edit `.env` with your API details.
3.  **Run:** Execute the script: `python src/tgspammer.py`
4.  **Follow prompts:** The script will request input to initiate the spamming process.

<hr>

## 📜 Full Documentation

For detailed instructions, feature explanations, consult the full [Documentation](docs/README.md).

<hr>

## ⚠️ Important Disclaimer: Liability Evasion Initiated

This tool is provided purely for "educational endeavors" and "network analysis." Use it responsibly and ethically.

**I bear no responsibility for any misuse of this digital tool, including but not limited to:**

*   Spamming anyone for any reason whatsoever.
*   Violating Telegram's Terms of Service.
*   Account restrictions or suspensions.
*   Any other form of digital aggravation you might inflict upon unwilling recipients.

<p align="center"> Proceed at your own risk and amusement. </p>

<hr>

## 📄 License

[MIT License](LICENSE) - A permissive license.
