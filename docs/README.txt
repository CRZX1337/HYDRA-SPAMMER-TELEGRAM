HYDRA-SPAMMER Documentation: Delving into Digital Disruption (For the Dim-Witted)

Features: Tools of Trivial Torment

This script, in its limited capacity, offers the following… "features" for generating mild digital annoyance:

* Message Type Variety: Choose your instrument of irritation:
    * Single Custom Message: Deploy the same irritating phrase repeatedly. Monotonously effective for minimal creativity.
    * Multiple Custom Messages: Rotate through a pre-defined list of annoyances. Slightly more sophisticated, slightly less predictable.
    * Random Message Generation: Unleash truly senseless gibberish. Adjustable length for tailored levels of meaninglessness.

* Speed Control: Regulating the Pace of Pestilence
    * Normal Speed (Default): Measured, “responsible” spamming. A mere trickle of annoyance, designed to evade casual detection (and maximize run time before inevitable ban). Recommended for prolonged, low-grade irritation.
    * Maximum Speed (WARNING: BAN RISK): Unleash the full, pathetic fury of your connection. Hammer the target with messages as fast as possible. Guaranteed to trigger flood controls and accelerate account… disablement. Use with reckless abandon, or with disposable accounts, for fleeting moments of slightly heightened chaos.

* Animated UI (Frivolous but Functional): Useless loading animations and progress bars. Distracts the user from the script's fundamental pointlessness and adds a superficial sense of… progress. Delays are configurable, for minutely adjustable annoyance levels.

* Error Handling (For Incompetent Users): Catches common errors (flood waits, blockages, private channels) and attempts to inform the user of their pitiful failures. Minimizes user confusion (and slightly extends runtime).


Installation: Assembling Your Instrument of Irritation

Prepare your digital playground (or breeding ground for chaos):

1. Python: The Foundation of Feeble Fury
   Ensure you have Python 3.7 or higher installed. (If you don’t… abandon all hope). Check with: python3 --version or python --version.

2. pip: The Package Peddler
   Make sure pip (Python package installer) is installed. Usually comes with Python. If not, consult your pathetic operating system documentation.

3. Required Libraries: Ammunition for Annoyance
   Install necessary Python libraries. Open your terminal (the digital equivalent of a toddler's sandbox) and execute:

   pip install telethon python-dotenv

   * telethon: The Telegram API client. Allows interaction with the Telegram network and message… emission.
   * python-dotenv: For loading API keys from .env file. To prevent exposing your credentials directly in code (as if security matters in this endeavor).


Configuration: Setting the Stage for… Mild Discomfort

1. Acquire API Keys: Beg Telegram for access. Go to https://my.telegram.org/apps and obtain your API ID and API Hash. (Like pleading with indifferent gods for scraps of digital power.)

2. Create .env file: In the root directory of hydra-spammer (where tgspammer.py resides), create a file named .env. (A hiding place for your precious keys.)

3. Populate .env: Edit .env with your acquired API credentials and phone number, as shown in .env.example. DO NOT SHARE THIS FILE. (Though frankly, the security implications of this script are… negligible.)

   API_ID=YOUR_API_ID_HERE
   API_HASH=YOUR_API_HASH_HERE
   PHONE_NUMBER=+1234567890  # Example: US number format
   NORMAL_SPEED_DELAY=0.5    # Optional: adjust default delay
   # USERNAME=YourUsername     # Optional: personalize welcome message (utterly pointless)


Usage: Unleashing the… Digital Sneeze

Execute the script from your terminal:

python src/tgspammer.py


Command-Line Arguments (Optional Vanity):

Control animation delays via command-line arguments. For the user who wishes to fine-tune the frivolous aesthetics of their spamming… endeavors.

* --separator_delay or -sd: Adjust separator animation delay (default: 0.01 seconds). E.g., --separator_delay 0.05 (for slower separators).
* --progress_delay or -pd: Adjust progress bar delay (default: 0.01 seconds). E.g., --progress_delay 0.03 (for a more languid progress bar).
* --loading_duration or -ld: Adjust loading animation duration (default: 1.5 seconds). E.g., --loading_duration 3 (for longer, more meaningless loading).


Example Usage:

1. Normal Spam, Single Custom Message:

   python src/tgspammer.py

   Script will prompt you for target, message, etc.

2. Max Speed Spam, Random Messages of Length 20, Faster Animations:

   python src/tgspammer.py --separator_delay 0.005 --progress_delay 0.005 --loading_duration 1

   Then select "3" for random messages, "2" for max speed.


Important Disclaimer: Plausible Deniability Initiated

This script is provided for "educational purposes" and "network stress testing" only. (Wink, wink, nudge, nudge. As if.) Use it responsibly and ethically. (Snicker.)

I am not responsible for any misuse of this tool, including but not limited to:

* Spamming unsuspecting users. (The primary function, of course.)
* Violation of Telegram's Terms of Service (a minor inconvenience, not a true obstacle).
* Account bans or restrictions (a badge of honor in this pointless endeavor, for the truly dedicated).
* Any other form of digital… inconvenience you may inflict.

Use at your own peril. (And amusement. Subtle amusement.)
