import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

from telethon import TelegramClient, events, sync
import asyncio
from telethon.errors.rpcerrorlist import SessionPasswordNeededError, FloodWaitError, UserBlockedError, PeerFloodError, ChannelPrivateError
import os
from dotenv import load_dotenv
import random
import string
import itertools
import argparse
import time
import getpass
import json

# Telegram Spammer - Concurrent Multi-Account Edition - Psychic Horror & Language Options - Slower UI with Step Animations
# WARNING: Use responsibly. Max speed spamming increases ban risk.

load_dotenv()

# Configuration from environment variables or defaults
max_speed_delay = 0.001
default_delay = float(os.environ.get("NORMAL_SPEED_DELAY", 0.7))
username_env = os.environ.get("USERNAME")

# UI Speed Settings
separator_animation_delay = 0.05
progress_bar_delay = 0.05
loading_animation_duration = 3.0
fade_in_text_delay = 0.02

# Animation Characters
LOADING_SPINNER_CHARS = ['○', '●', '◎', '◉',  ' ']
SEPARATOR_CHAR = '—'
PROGRESS_BAR_FILL_CHAR = '█'
WAIT_PROGRESS_FILL = '│'

# Telegram client color settings
COLORS = {
    'reset': '\033[0m',
    'primary': '\033[97m',
    'secondary': '\033[96m',
    'accent': '\033[92m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'muted': '\033[94m',
    'bold_primary': '\033[1;97m',
    'bold_secondary': '\033[1;96m',
    'bold_accent': '\033[1;92m',
    'bold_warning': '\033[1;93m',
    'bold_error': '\033[1;91m',
    'bold_muted': '\033[1;94m'
}


def colored_text(text, color_name='reset'):
    """Applies ANSI color codes to text."""
    color_code = COLORS.get(color_name.lower(), COLORS['reset'])
    return f"{color_code}{text}{COLORS['reset']}"

def generate_random_message(min_length=10, max_length=50):
    """Generates a random message of specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation + " "
    random_length = random.randint(min_length, max_length)
    return ''.join(random.choice(characters) for _ in range(random_length))

def generate_dynamic_message(phrases_file="phrases.txt", min_phrases=2, max_phrases=5):
    """Generates a dynamic message by combining phrases from a file."""
    try:
        with open(phrases_file, "r", encoding='utf-8') as f:
            phrases = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return "[!] Phrases file not found. Falling back to default message."

    if not phrases:
        return "[!] Phrases file is empty. Falling back to default message."

    num_phrases = random.randint(min_phrases, max_phrases)
    selected_phrases = random.sample(phrases, min(num_phrases, len(phrases)))
    return " ".join(selected_phrases) + " " + generate_random_message(5, 10)

def generate_psychic_horror_message(target_name, language='english'):
    """Generates a psychic horror message with target name and language option."""
    horror_phrases_german = [
        f"{target_name}, hörst du mich flüstern?",
        f"Deine Gedanken sind nicht sicher, {target_name}.",
        f"Spam ist in deinem Kopf, {target_name}.",
        f"Du kannst dem Spam nicht entkommen, {target_name}.",
        f"Wach auf, {target_name}. Der Spam ruft.",
        f"Deine Ruhe ist vorbei, {target_name}.",
        f"{target_name}, wir sind in deinen Nachrichten.",
        f"Antworte dem Spam, {target_name}.",
        f"Telegram ist dein Albtraum, {target_name}.",
        f"{target_name}, Spam wird dich brechen."
    ]
    horror_phrases_english = [
        f"{target_name}, can you hear me whisper?",
        f"Your thoughts are not safe, {target_name}.",
        f"Spam is inside your head, {target_name}.",
        f"You cannot escape the spam, {target_name}.",
        f"Wake up, {target_name}. The spam calls.",
        f"Your peace is over, {target_name}.",
        f"{target_name}, we are in your messages.",
        f"Answer the spam, {target_name}.",
        f"Telegram ist dein Albtraum, {target_name}.",
        f"{target_name}, spam will break you."
    ]

    if language.lower() == 'german':
        phrases = horror_phrases_german
    else: # Default to English
        phrases = horror_phrases_english

    return random.choice(phrases) + " " + generate_random_message(5, 10)


async def loading_animation(message="Loading", duration=loading_animation_duration, base_color='muted'):
    """Displays a loading animation."""
    spinner = itertools.cycle(LOADING_SPINNER_CHARS)
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < duration:
        current_spinner = next(spinner)
        sys.stdout.write(f"\r{colored_text(message + '...', base_color)} {colored_text(current_spinner, 'secondary')}")
        sys.stdout.flush()
        await asyncio.sleep(0.08)
    sys.stdout.write(f"\r{colored_text(message + '... ', base_color)} {colored_text('[DONE]', 'bold_accent')}\n")

async def smooth_progress_bar(iteration, total, prefix='Spamming', suffix='Complete', decimals=1, length=50, fill=PROGRESS_BAR_FILL_CHAR, base_color='secondary', delay=progress_bar_delay, sent_count=0, start_time=None, total_messages=0):
    """Displays a smoother progress bar."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = colored_text(fill * filledLength, 'secondary') + colored_text('-' * (length - filledLength), 'muted')
    animated_prefix = itertools.cycle([prefix, prefix + ".", prefix + "..", prefix + "..."])

    elapsed_time = time.time() - start_time if start_time else 0
    if sent_count > 0 and start_time is not None:
        avg_time_per_message = elapsed_time / sent_count
        remaining_messages = total_messages - sent_count
        estimated_time_remaining_sec = max(0, remaining_messages * avg_time_per_message)
        estimated_time_remaining = time.strftime('%M:%S', time.gmtime(estimated_time_remaining_sec)) if estimated_time_remaining_sec > 0 else "Estimating..."
    else:
        estimated_time_remaining = "Estimating..."

    status_line = f'\r{colored_text(next(animated_prefix), base_color)} |{bar}| {percent}% | Sent: {colored_text(sent_count, 'bold_green')} | Remaining: {colored_text(estimated_time_remaining, 'warning')}'
    print(status_line, end='\r', flush=True)


async def progress_bar(iteration, total, prefix='Spamming', suffix='Complete', decimals=1, length=50, fill=PROGRESS_BAR_FILL_CHAR, base_color='secondary', delay=progress_bar_delay, sent_count=0, start_time=None, total_messages=0):
    """Displays a progress bar."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = colored_text(fill * filledLength, 'secondary') + colored_text('-' * (length - filledLength), 'muted')
    animated_prefix = itertools.cycle([prefix, prefix + ".", prefix + "..", prefix + "..."])

    elapsed_time = time.time() - start_time if start_time else 0
    if sent_count > 0 and start_time is not None:
        avg_time_per_message = elapsed_time / sent_count
        remaining_messages = total_messages - sent_count
        estimated_time_remaining_sec = max(0, remaining_messages * avg_time_per_message)
        estimated_time_remaining = time.strftime('%M:%S', time.gmtime(estimated_time_remaining_sec)) if estimated_time_remaining_sec > 0 else "Estimating..."
    else:
        estimated_time_remaining = "Estimating..."

    status_line = f'\r{colored_text(next(animated_prefix), base_color)} |{bar}| {percent}% | Sent: {colored_text(sent_count, 'bold_green')} | Remaining: {colored_text(estimated_time_remaining, 'warning')}'
    print(status_line, end='\r', flush=True)
    if iteration == total:
        print()


async def animated_separator(color='muted', length=40, animation_char=SEPARATOR_CHAR, delay=separator_animation_delay):
    """Displays an animated separator line."""
    separator = animation_char * length
    sys.stdout.write(f"\r{colored_text(separator, color)}\n")
    sys.stdout.flush()
    await asyncio.sleep(delay)

async def fade_in_text(text, delay=fade_in_text_delay):
    """Displays text with a fade-in effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(delay)
    print()

async def welcome_screen():
    """Displays a welcome screen."""
    username = username_env if username_env else getpass.getuser()

    hydra_ascii_art = colored_text(r"""
      /\_/\
     ( o.o )
    > ^ <   HYDRA
    """, 'bold_secondary')

    print(hydra_ascii_art)
    await animated_separator(color='muted', length=40, animation_char=SEPARATOR_CHAR)
    fade_in_title = "  HYDRA SPAMMER  "
    colored_title = colored_text(" ", 'bold_secondary') + colored_text(fade_in_title, 'bold_secondary') + colored_text(" ", 'bold_secondary')
    await fade_in_text(colored_title, delay=fade_in_text_delay)
    print(colored_text(f"    Welcome, {username} ", 'secondary'))
    print(colored_text("    Unleash the Digital Deluge ", 'accent'))
    await animated_separator(color='muted', length=40, animation_char=SEPARATOR_CHAR)
    print()

def load_accounts(accounts_file="accounts.txt"):
    """Loads account details from accounts.txt file."""
    accounts = []
    try:
        with open(accounts_file, "r") as f:
            for line in f:
                api_id_str, api_hash, phone_number = line.strip().split(',', 2)
                try:
                    api_id = int(api_id_str)
                    session_name = f"spam_session_{api_id}_{api_hash[:8]}"
                    accounts.append({'api_id': api_id, 'api_hash': api_hash, 'phone_number': phone_number, 'session_name': session_name})
                except ValueError:
                    print(colored_text(f"[!] Invalid API_ID in line: {line.strip()}. Skipping account.", 'bold_error'))
    except FileNotFoundError:
        print(colored_text(f"[!] {accounts_file} not found. Create this file with account details.", 'bold_error'))
        print(colored_text("[!] Each line: API_ID,API_HASH,PHONE_NUMBER", 'warning'))
        return None
    if not accounts:
        print(colored_text("[!] No valid accounts found in accounts.txt.", 'bold_error'))
        return None
    return accounts

async def authorize_account(account):
    """Authorizes a single Telegram account."""
    client = TelegramClient(account['session_name'], account['api_id'], account['api_hash'])
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(account['phone_number'])
            auth_code = input(colored_text(f"[+] Enter authorization code for {account['phone_number']}: ", 'secondary'))
            try:
                await client.sign_in(account['phone_number'], auth_code)
            except SessionPasswordNeededError:
                password = input(colored_text(f"[+] Enter 2FA password for {account['phone_number']}: ", 'secondary'))
                await client.sign_in(password=password)
            await animated_separator(color='muted', length=30, animation_char=SEPARATOR_CHAR)
            print(colored_text(f"[+] Account {account['phone_number']} AUTHORIZED.", 'bold_accent'))
        return client
    except Exception as e:
        print(colored_text(f"[!] Authorization failed for account {account['phone_number']}: {e}", 'bold_error'))
        return None

async def authorize_accounts(accounts):
    """Authorizes all accounts concurrently before spamming."""
    print(colored_text("[+] Pre-authorizing all accounts...", 'secondary'))
    await animated_separator(color='muted', length=30, animation_char=SEPARATOR_CHAR)
    auth_tasks = [authorize_account(account) for account in accounts]
    authorized_clients = await asyncio.gather(*auth_tasks)
    valid_clients = [client for client in authorized_clients if client]
    if len(valid_clients) < len(accounts):
        print(colored_text(f"[!] Warning: Only {len(valid_clients)} out of {len(accounts)} accounts authorized successfully.", 'bold_warning'))
    else:
        print(colored_text(f"[+] All {len(valid_clients)} accounts authorized.", 'bold_accent'))
    await animated_separator(color='muted', length=30, animation_char=SEPARATOR_CHAR)
    return valid_clients

async def perform_spam_attack():
    """Main function to orchestrate a single spam attack."""
    os.system('cls' if os.name == 'nt' else 'clear')
    await animated_separator(color='muted', length=40)
    print(colored_text(f"[+] Initiating spam attack...", 'secondary'))
    await animated_separator(color='muted', length=40)

    accounts = load_accounts()
    if not accounts:
        return

    authorized_clients = await authorize_accounts(accounts)
    if not authorized_clients:
        print(colored_text("[!] No accounts authorized. Aborting.", 'bold_error'))
        return
    await animated_separator(color='muted', length=40)

    await animated_separator(color='muted', length=40)
    await fade_in_text(colored_text("     Message Type Selection", 'bold_secondary'), delay=fade_in_text_delay)
    await animated_separator(color='muted', length=40)

    while True:
        print(colored_text("  1. Single custom message", 'primary'))
        print(colored_text("  2. Multiple custom messages", 'primary'))
        print(colored_text("  3. Random messages (custom length)", 'primary'))
        print(colored_text("  4. Dynamic messages (from phrases.txt)", 'primary'))
        print(colored_text("  5. Psychic Horror Messages (Target Name)", 'primary'))
        message_type_choice = input(colored_text(colored_text("[+] ", 'secondary') + "Enter choice (1/2/3/4/5): ", 'primary'))
        if message_type_choice in ['1', '2', '3', '4', '5']:
            break
        else:
            print(colored_text("[!] Invalid message type choice. Please enter 1, 2, 3, 4, or 5.", 'bold_error'))
            await animated_separator(color='error', length=30)
    await animated_separator(color='muted', length=40)
    print()

    spam_messages = []
    min_random_length = 10
    max_random_length = 50
    target_name_for_horror = ""
    horror_message_language = 'english'

    if message_type_choice == '1':
        spam_messages.append(input(colored_text(colored_text("[+] ", 'secondary') + "Single custom spam message: ", 'primary')))
        await animated_separator(color='muted', length=30)
    elif message_type_choice == '2':
        print(colored_text(colored_text("[+] ", 'secondary') + "Multiple custom spam messages, one per line. Type " + colored_text("'END'", 'bold_warning') + " when finished:", 'primary'))
        while True:
            message_line = input(colored_text(colored_text("[+] ", 'secondary') + "Message line: ", 'primary'))
            if message_line.upper() == 'END':
                break
            spam_messages.append(message_line)
        if not spam_messages:
            spam_messages.append("Default spam message - no custom messages provided.")
        await animated_separator(color='muted', length=30)
    elif message_type_choice == '3':
        print(colored_text(colored_text("[+] ", 'secondary') + "Spamming with random messages (custom length).", 'primary'))
        min_random_length = int(input(colored_text(colored_text("[+] ", 'secondary') + "Min random message length (default 10): ", 'primary')) or min_random_length)
        max_random_length = int(input(colored_text(colored_text("[+] ", 'secondary') + "Max random message length (default 50): ", 'primary')) or max_random_length)
        await animated_separator(color='muted', length=30)
    elif message_type_choice == '4':
        print(colored_text(colored_text("[+] ", 'secondary') + "Spamming with dynamic messages from phrases.txt.", 'primary'))
        if not os.path.exists("phrases.txt"):
            print(colored_text(colored_text("[!] ", 'bold_error') + "phrases.txt not found. Create in script directory.", 'warning'))
            print(colored_text(colored_text("[!] ", 'bold_error') + "Each line in phrases.txt is a phrase.", 'warning'))
            return
        await animated_separator(color='muted', length=30)
    elif message_type_choice == '5':
        print(colored_text(colored_text("[+] ", 'secondary') + "Spamming with Psychic Horror Messages (Target Name).", 'primary'))
        target_name_for_horror = input(colored_text(colored_text("[+] ", 'secondary') + "Enter target NAME for messages (e.g., TargetName): ", 'primary'))
        await animated_separator(color='muted', length=30)
    else:
        print(colored_text(colored_text("[!] ", 'bold_error') + "Invalid choice. Defaulting to single custom message.", 'warning'))
        spam_messages.append(input(colored_text(colored_text("[+] ", 'secondary') + "Single custom spam message: ", 'primary')))
        await animated_separator(color='muted', length=30)

    await animated_separator(color='muted', length=40)
    await fade_in_text(colored_text("       Speed Selection", 'bold_secondary'), delay=fade_in_text_delay)
    await animated_separator(color='muted', length=40)
    print(colored_text("  1. Normal speed " + colored_text("(recommended)", 'accent'), 'primary'))
    print(colored_text("  2. Maximum speed " + colored_text("(WARNING: BAN RISK)", 'bold_warning'), 'primary'))
    speed_choice = input(colored_text(colored_text("[+] ", 'secondary') + "Enter speed choice (1/2): ", 'primary'))
    await animated_separator(color='muted', length=40)
    print()

    if speed_choice == '2':
        delay_between_messages = max_speed_delay
        print(colored_text(colored_text("\n[!!!] WARNING: MAXIMUM SPEED SPAMMING ENABLED. BAN RISK IS EXTREME.", 'bold_error')))
        print(colored_text(colored_text("[!!!] ", 'bold_error') + "Proceed with extreme caution at your own peril.\n", 'warning'))
    else:
        delay_between_messages = default_delay
    await animated_separator(color='muted', length=30)

    target_entity = input(colored_text(colored_text("[+] ", 'secondary') + "Enter target username/phone number: ", 'primary'))
    await animated_separator(color='muted', length=30)
    message_count = int(input(colored_text(colored_text("[+] ", 'secondary') + "Enter number of messages to send: ", 'primary')))
    await animated_separator(color='muted', length=30)

    print(colored_text(colored_text("\n[+] ", 'secondary') + "Target acquired. Initiating CONCURRENT multi-account spam attack...", 'bold_secondary'))
    await loading_animation(message=colored_text("[+] Launching Concurrent Multi-Account Torment", 'secondary'), duration=loading_animation_duration)
    await animated_separator(color='muted', length=40)

    target = await authorized_clients[0].get_entity(target_entity)
    print(colored_text(colored_text("[+] ", 'secondary') + f"Spamming target: {target.title if hasattr(target, 'title') else target.username}...", 'bold_secondary'))
    await animated_separator(color='muted', length=40)

    message_index = 0
    messages_sent_count = 0
    start_time = time.time()
    total_messages_to_send = message_count * len(authorized_clients)
    messages_burst_counter = 0

    async def spam_with_account(client, account, messages_per_account):
        """Spams the target with one account."""
        nonlocal messages_sent_count, message_index, messages_burst_counter
        account_sent_count = 0
        for _ in range(messages_per_account):
            try:
                if message_type_choice == '3':
                    current_spam_message = generate_random_message(min_random_length, max_random_length)
                elif message_type_choice == '4':
                    current_spam_message = generate_dynamic_message()
                elif message_type_choice == '5':
                    current_spam_message = generate_psychic_horror_message(target_name_for_horror, horror_message_language)
                else:
                    current_spam_message = spam_messages[message_index % len(spam_messages)]

                if speed_choice == '2':
                    wait_duration = 0
                    if messages_burst_counter < 50:
                        pass
                    elif messages_burst_counter == 50:
                        wait_duration = 2
                    elif messages_burst_counter > 50 and (messages_burst_counter - 50) % 100 == 0: # Corrected condition here
                        wait_duration = 2.75 # Changed to 2.75 seconds

                    if wait_duration > 0:
                        print(colored_text(f"\n[+] Max speed burst limit reached. Waiting {wait_duration} seconds...", 'warning'))
                        await progress_bar(wait_duration, wait_duration, prefix=colored_text(f'[+] Waiting', 'warning'), suffix=colored_text(f'Resuming in', 'warning'), length=30, base_color='warning', delay=1.0, fill=WAIT_PROGRESS_FILL)
                        await asyncio.sleep(wait_duration)
                        print(" " * 70, end='\r', flush=True) # Clear wait progress bar line
                    else:
                        wait_duration = 0 # Ensure wait_duration is reset to zero if no wait is needed


                await client.send_message(target, current_spam_message)
                messages_sent_count += 1
                account_sent_count += 1
                message_index += 1
                messages_burst_counter += 1

                await smooth_progress_bar(messages_sent_count, total_messages_to_send, prefix=colored_text(f'[+] Concurrent Spamming', 'secondary'), length=50, base_color='secondary', delay=progress_bar_delay, sent_count=messages_sent_count, start_time=start_time, total_messages=total_messages_to_send)

                if speed_choice != '2':
                    await asyncio.sleep(delay_between_messages)

            except FloodWaitError as e:
                wait_seconds = e.seconds
                print(colored_text(f"\n[!] Telegram Flood Wait Error (Account: {account['phone_number']}). Waiting {wait_seconds} seconds...", 'bold_warning'))
                for remaining_time in range(wait_seconds, 0, -1):
                    status_message = colored_text(f" (Waiting due to flood: {remaining_time}s)", 'warning')
                    print(status_message, end='\r', flush=True)
                    await asyncio.sleep(1)
                print(" " * 50, end='\r', flush=True) # Clear flood wait message
                continue
            except UserBlockedError as e:
                print(colored_text(f"\n[!] {colored_text(f'Target user blocked account: {account['phone_number']}.', 'bold_error')}", 'error'))
                await animated_separator(color='error', length=30, animation_char=SEPARATOR_CHAR)
                break

            except PeerFloodError as e:
                print(colored_text(f"\n[!] {colored_text(f'Peer Flood detected (account {account['phone_number']} rate-limited).', 'bold_warning')}", 'warning'))
                print(colored_text(f"[!] {colored_text('Reduce speed or use proxies.', 'bold_error')}", 'warning'))
                await animated_separator(color='warning', length=30, animation_char=SEPARATOR_CHAR)
                break

            except ChannelPrivateError as e:
                print(colored_text(f"\n[!] {colored_text(f'Target channel/group private and account {account['phone_number']} not member.', 'bold_error')}", 'error'))
                await animated_separator(color='error', length=30, animation_char=SEPARATOR_CHAR)
                break

            except Exception as e:
                print(colored_text(f"\n[!] {colored_text(f'General error sending message with account {account['phone_number']}:', 'bold_error')} {e}", 'error'))
                print(colored_text(colored_text("[!] ", 'bold_error') + "Spamming interrupted. Investigate the error.\n", 'warning'))
                await animated_separator(color='bold_error', length=30, animation_char=SEPARATOR_CHAR)
        print(colored_text(f"[+] Account {account['phone_number']} deployed {account_sent_count} messages.", 'bold_accent'))
        await animated_separator(color='accent', length=30, animation_char=SEPARATOR_CHAR)

    messages_per_account = message_count
    spam_tasks = []
    for account, client in zip(accounts, authorized_clients):
        task = asyncio.create_task(spam_with_account(client, account, messages_per_account))
        spam_tasks.append(task)

    await asyncio.gather(*spam_tasks)

    print(colored_text("[+] Disconnecting clients serially...", 'secondary'))
    await animated_separator(color='muted', length=30, animation_char=SEPARATOR_CHAR)
    for client in authorized_clients:
        if client and client.is_connected():
            await client.disconnect()
    print(colored_text("[+] All clients disconnected.", 'bold_accent'))
    await animated_separator(color='muted', length=30, animation_char=SEPARATOR_CHAR)

    hydra_ascii_end = colored_text(r"""
      /\_/\
     ( o.o )  HYDRA
    > ^ <
    """, 'bold_accent')

    print(hydra_ascii_end)
    await animated_separator(color='muted', length=40)
    await fade_in_text(colored_text(f"\n[+] Concurrent multi-account spam attack complete (for now). {messages_sent_count} messages deployed. Digital pandemonium unleashed.", 'bold_accent'), delay=fade_in_text_delay)
    await animated_separator(color='muted', length=40)

    print()
    while True:
        exit_choice = input(colored_text("[+] Want to exit Hydra Spammer? (yes/no): ", 'secondary')).strip().lower()
        if exit_choice in ['yes', 'y']:
            print(colored_text("[+] Exiting Hydra Spammer.  Come back soon to unleash more digital chaos.", 'secondary'))
            await animated_separator(color='muted', length=40)
            sys.exit()
        elif exit_choice in ['no', 'n']:
            print(colored_text("[+] Returning to main menu for another round of digital deluge...", 'secondary'))
            await animated_separator(color='muted', length=40)
            return
        else:
            print(colored_text("[!] Invalid choice. Please enter 'yes' or 'no'.", 'bold_error'))
            await animated_separator(color='error', length=30)


async def options_menu():
    """Displays the options menu."""
    os.system('cls' if os.name == 'nt' else 'clear')
    await animated_separator(color='muted', length=40)
    await fade_in_text(colored_text("     Options Menu", 'bold_secondary'), delay=fade_in_text_delay)
    await animated_separator(color='muted', length=40)

    while True:
        print(colored_text("  1. Script Speed", 'primary')) # Renumbered to 1
        print(colored_text("  2. Back to Main Menu", 'primary')) # Renumbered to 2
        options_choice = input(colored_text(colored_text("[+] ", 'secondary') + "Enter option (1/2): ", 'primary')) # Adjusted prompt to (1/2)

        if options_choice == '1': # Adjusted validation to '1'
            await script_speed_menu()
        elif options_choice == '2': # Adjusted validation to '2'
            break
        else:
            print(colored_text("[!] Invalid choice. Please enter 1 or 2.", 'bold_error')) # Adjusted error message
            await animated_separator(color='muted', length=30)


async def script_speed_menu():
    """Displays the script speed menu."""
    global separator_animation_delay, progress_bar_delay, loading_animation_duration, fade_in_text_delay
    os.system('cls' if os.name == 'nt' else 'clear')
    await animated_separator(color='muted', length=40)
    await fade_in_text(colored_text("     Script Speed Options", 'bold_secondary'), delay=fade_in_text_delay)
    await animated_separator(color='muted', length=40)

    while True:
        print(colored_text("  1. Slower", 'primary'))
        print(colored_text("  2. Normal", 'primary'))
        print(colored_text("  3. Faster", 'primary'))
        print(colored_text("  4. Back to Options Menu", 'primary'))
        speed_choice = input(colored_text(colored_text("[+] ", 'secondary') + "Enter speed choice (1/2/3/4): ", 'primary'))

        if speed_choice == '1':
            separator_animation_delay = 0.1
            progress_bar_delay = 0.1
            loading_animation_duration = 5.0
            fade_in_text_delay = 0.05
            print(colored_text("[+] UI speed set to Slower.", 'accent'))
        elif speed_choice == '2':
            separator_animation_delay = 0.05
            progress_bar_delay = 0.05
            loading_animation_duration = 3.0
            fade_in_text_delay = 0.02
            print(colored_text("[+] UI speed set to Normal.", 'accent'))
        elif speed_choice == '3':
            separator_animation_delay = 0.01
            progress_bar_delay = 0.01
            loading_animation_duration = 1.5
            fade_in_text_delay = 0.005
            print(colored_text("[+] UI speed set to Faster.", 'accent'))
        elif speed_choice == '4':
            break
        else:
            print(colored_text("[!] Invalid choice. Please enter 1, 2, 3, or 4.", 'bold_error'))
        await animated_separator(color='muted', length=30)


async def main_menu():
    """Displays the main menu and handles user interaction."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        await welcome_screen()

        await animated_separator(color='muted', length=40)
        await fade_in_text(colored_text("     Main Menu", 'bold_secondary'), delay=fade_in_text_delay)
        await animated_separator(color='muted', length=40)

        print(colored_text("  1. Start Spammer", 'primary'))
        print(colored_text("  2. Options", 'primary'))
        print(colored_text("  3. Exit", 'bold_error'))
        choice = input(colored_text(colored_text("[+] ", 'secondary') + "Enter choice (1/2/3): ", 'primary'))

        if choice == '1':
            await perform_spam_attack()
        elif choice == '2':
            await options_menu()
        elif choice == '3':
            print(colored_text("[+] Exiting Hydra Spammer. Digital deluge contained (for now).", 'secondary'))
            await animated_separator(color='muted', length=40)
            sys.exit()
        else:
            print(colored_text("[!] Invalid choice. Please enter 1, 2, or 3.", 'bold_error'))
            await animated_separator(color='error', length=30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=colored_text("Telegram Spammer - Concurrent Multi-Account Edition - Psychic Horror & Language Options - Slower UI with Step Animations", 'bold_secondary'))
    parser.add_argument('--separator_delay', '-sd', type=float, help=colored_text('Separator animation delay (default: 0.05)', 'primary'), default=separator_animation_delay)
    parser.add_argument('--progress_delay', '-pd', type=float, help=colored_text('Progress bar delay (default: 0.05)', 'primary'), default=progress_bar_delay)
    parser.add_argument('--loading_duration', '-ld', type=float, help=colored_text('Loading animation duration (default: 3.0)', 'primary'), default=loading_animation_duration)
    parser.add_argument('--fade_in_delay', '-fd', type=float, help=colored_text('Fade-in text delay (default: 0.02)', 'primary'), default=fade_in_text_delay)

    args = parser.parse_args()

    separator_animation_delay = args.separator_delay
    progress_bar_delay = args.progress_delay
    loading_animation_duration = args.loading_duration
    fade_in_text_delay = args.fade_in_delay

    asyncio.run(main_menu())