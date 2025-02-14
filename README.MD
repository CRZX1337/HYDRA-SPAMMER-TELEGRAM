# <div align="center"> 😈 HYDRA-SPAMMER: Digital Torment - Concurrent Edition Unleashed 😈 </div>
<p align="center">

</p>
<br>

<div align="center">
    <h3> Unleash a Legion of Digital… <ins>Annoyance</ins> Concurrently upon Telegram Targets </h3>
</div>

<p align="center">
    HYDRA-SPAMMER - Concurrent Edition is a significantly enhanced Python-based Telegram spamming tool, now capable of deploying message torrents from <ins>multiple accounts simultaneously</ins> for "stress testing," "educational purposes," and activities requiring <ins>mass message dissemination</ins>.
</p>

<hr>

## 📸 Preview Screenshots:

<div align="center">
    <img src="https://github.com/CRZX1337/HYDRA-SPAMMER-TELEGRAM/blob/main/preview1.png" width="400" alt="Hydra-Spammer Preview Screenshot 1">
    <br>
    <br>
    <img src="https://github.com/CRZX1337/HYDRA-SPAMMER-TELEGRAM/blob/main/preview2.png" width="400" alt="Hydra-Spammer Preview Screenshot 2">
    <br>
    <br>
    <img src="https://github.com/CRZX1337/HYDRA-SPAMMER-TELEGRAM/blob/main/preview3.png" width="400" alt="Hydra-Spammer Multi-Account Preview">
</div>

<hr>

## ⚙️ Key Features: Legion of Irritation

This script, in its amplified form, provides instruments for generating a more substantial digital discomfort:

*   **🐙 Concurrent Multi-Account Spam:**
    *   Harness the power of **multiple Telegram accounts** to send messages **simultaneously**.
    *   Dramatically **increases spam volume** and potential impact.
    *   Distributes workload across accounts.

*   **🎭 Versatile Message Types:** (Inherited from previous feeble versions, now amplified)
    *   **Single Custom Message:** Deploy the same monotonous phrase repeatedly across all accounts.
    *   **Multiple Custom Messages:** Cycle through a list of pre-scripted messages, rotated across all accounts.
    *   **🎲 Random Message Generation:** Unleash truly senseless gibberish of adjustable length from each account.
    *   **✨ Dynamic Message Generation:** Create varied and unpredictable messages by combining phrases from `phrases.txt`, now deployed concurrently from every account.

*   **⏱️ Adjustable Speed Modes:** Regulate the amplified message torrent:
    *   **🐢 Normal Speed (Default):**  A slower, more "responsible" message stream across all accounts. Minimizes immediate detection (slightly).
    *   **🚀 Maximum Speed (⚠️ WARNING: EXTREME BAN RISK ⚠️):** Unleash the combined, pathetic fury of *all* your accounts simultaneously.  Guaranteed to trigger flood controls and accelerate account… incineration.  For fleeting moments of maximum, reckless chaos.

*   **✨ Animated User Interface:** (Still frivolous, but now for a legion of spam)
    *   Includes loading animations and progress bars, now reflecting the scale of multi-account operation.
    *   Animation delays remain configurable.

*   **🛡️ Error Handling:** (Slightly more robust for multi-account operations)
    *   Error handling for common Telegram API issues (FloodWait, Blockages, Private Channels) is extended to manage multi-account scenarios.

<hr>

## 🛠️ Installation: Assembling Your Legion

Prepare your environment for commanding a legion of digital annoyance:

1.  **🐍 Python:** Ensure you have Python 3.7 or higher installed. Verify with: `python3 --version` or `python --version`.

2.  **📦 pip:** Confirm `pip` (Python package installer) is installed.

3.  **📚 Libraries:** Install necessary Python libraries using `pip`:

    ```bash
    pip install telethon python-dotenv
    ```
    *   `telethon`: The Telegram API client, crucial for controlling your digital legion.
    *   `python-dotenv`: Still technically supported for optional settings, but account details are now managed via `accounts.txt`.

<hr>

## ⚙️ Configuration: Mobilizing the Legion

1.  **🔑 Telegram API Keys:**  Acquire API access credentials from Telegram: [https://my.telegram.org/apps](https://my.telegram.org/apps). Obtain your `API ID` and `API Hash` for *each* account you intend to deploy.

2.  **📝 Create `accounts.txt` file:**  In the root directory of `hydra-spammer`, create a file named `accounts.txt`. **This is now MANDATORY for multi-account operation.**

3.  **✍️ Populate `accounts.txt`:** Edit `accounts.txt` with your API credentials and phone numbers for **each account**, referencing the `accounts.txt.example` template. **Keep this file highly secure.**

    ```text
    # accounts.txt - Example (replace with your actual account details)
    API_ID_ACCOUNT_1,API_HASH_ACCOUNT_1,+PHONE_NUMBER_ACCOUNT_1
    API_ID_ACCOUNT_2,API_HASH_ACCOUNT_2,+PHONE_NUMBER_ACCOUNT_2
    # Add more accounts below, one per line, following the format...
    ```

4.  **📝 (Optional) `phrases.txt` file:** For dynamic message spam, create `phrases.txt` in the root directory. Add phrases, one per line, for dynamic message generation.

5.  **📝 (Optional) `.env` file:** The `.env` file is now *optional* and primarily for customizing `NORMAL_SPEED_DELAY` and `USERNAME` (for advanced aesthetic customization only). See `.env.example`.

    ```
    NORMAL_SPEED_DELAY=0.75   # Optional: Adjust default delay (seconds)
    # USERNAME=LegionCommander # Optional: Personalize welcome message (utterly insignificant)
    ```

<hr>

## 🚀 Quick Start: Unleash the Horde

1.  **Clone:** Clone this repository: `git clone [repository URL - *your responsibility to provide this* ]`
2.  **Configure Accounts:**  **MANDATORY:** Edit `accounts.txt` with your *multiple* API details.
3.  **Run:** Execute the script: `python tgspammer.py`
4.  **Authorize Accounts:**  The script will now prompt for authorization codes and 2FA passwords for **ALL** accounts at startup.  Authorize each when prompted.
5.  **Follow prompts:** The script will then request input to initiate the concurrent spamming process across your legion of accounts.

<hr>

## 📜 Full Documentation

For comprehensive instructions, feature explanations, and advanced usage details, consult the full [Documentation](docs/README.md).  (Still woefully inadequate, but sufficient for the dim-witted followers you will inevitably attract.)

<hr>

## ⚠️ Important Disclaimer: Legion Liability Evasion Engaged

This instrument of digital annoyance, now amplified for multi-account deployment, is provided purely for "educational endeavors," "network stress testing," and demonstrations of… *digital marketing potential*.  Use it with extreme caution and ethical… *flexibility*.

**I bear absolutely no responsibility for any misuse of this massively enhanced digital tool, including but not limited to:**

*   Spamming anyone for any conceivable reason, now with amplified and concurrent force.
*   Large-scale violations of Telegram's Terms of Service across multiple accounts, potentially attracting greater… *attention*.
*   Account restrictions, suspensions, or outright terminations across your entire digital legion.
*   Any form of digital aggravation, disruption, or outright chaos you might unleash upon a wider, more unsuspecting range of recipients.

<p align="center"> Deploy your legion at your own amplified risk and amplified amusement. </p>

<hr>

## 📄 License

[MIT License](LICENSE) - A license as permissive and ethically flexible as the tool itself.
