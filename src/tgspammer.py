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

# Telegram Spammer - Concurrent Multi-Account Edition
# WARNING: Use responsibly. Max speed spamming increases ban risk.

load_dotenv()

# Configuration from environment variables or defaults
max_speed_delay = 0.001  # Minimum delay for maximum speed
default_delay = float(os.environ.get("NORMAL_SPEED_DELAY", 0.5)) # Default delay between messages
username_env = os.environ.get("USERNAME") # Optional username for welcome message

separator_animation_delay = 0.01 # Delay for separator animation
progress_bar_delay = 0.01 # Delay for progress bar updates
loading_animation_duration = 1.5 # Duration of loading animations

# Telegram client color settings for terminal output
COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold_red': '\033[1;91m',
    'bold_green': '\033[1;92m',
    'bold_yellow': '\033[1;93m',
    'bold_blue': '\033[1;94m',
    'bold_magenta': '\033[1;95m',
    'bold_cyan': '\033[1;96m',
    'bold_white': '\033[1;97m'
}

def colored_text(text, color_name='reset'):
    """Applies ANSI color codes to text for terminal output."""
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

async def loading_animation(message="Loading", duration=loading_animation_duration, base_color='cyan'):
    """Displays a loading animation in the terminal."""
    spinner = itertools.cycle(['█', '▓', '▒', '░', ' '])
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < duration:
        current_spinner = next(spinner)
        sys.stdout.write(f"\r{colored_text(message + '...', base_color)} {colored_text(current_spinner, 'cyan')}")
        sys.stdout.flush()
        await asyncio.sleep(0.08)
    sys.stdout.write(f"\r{colored_text(message + '... ', base_color)} {colored_text('[DONE]', 'bold_green')}\n")

async def progress_bar(iteration, total, prefix='Spamming', suffix='Complete', decimals=1, length=50, fill='█', base_color='cyan', delay=progress_bar_delay, sent_count=0, estimated_time_remaining="N/A"):
    """Displays a progress bar in the terminal."""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = colored_text(fill * filledLength, 'cyan') + colored_text('-' * (length - filledLength), 'white')
    animated_prefix = itertools.cycle([prefix, prefix + ".", prefix + "..", prefix + "..."])
    status_line = f'\r{colored_text(next(animated_prefix), base_color)} |{bar}| {percent}% | Sent: {colored_text(sent_count, 'bold_green')} | Remaining: {colored_text(estimated_time_remaining, 'yellow')}'
    print(status_line, end='\r', flush=True)
    if iteration == total:
        print()

async def animated_separator(color='cyan', length=40, animation_char='█', delay=separator_animation_delay):
    """Displays an animated separator line in the terminal."""
    separator = animation_char * length
    sys.stdout.write(f"\r{colored_text(separator, color)}\n")
    sys.stdout.flush()
    await asyncio.sleep(delay)

async def fade_in_text(text, delay=0.005):
    """Displays text with a fade-in effect in the terminal."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(delay)
    print()

async def welcome_screen():
    """Displays a welcome screen with script title and user information."""
    username = username_env if username_env else getpass.getuser()
    await animated_separator(color='bold_cyan', length=40, animation_char='▓')
    fade_in_title = "  HYDRA SPAMMER  "
    colored_title = colored_text(" ", 'bold_magenta') + colored_text(fade_in_title, 'bold_magenta') + colored_text(" ", 'bold_magenta')
    await fade_in_text(colored_title, delay=0.02)
    print(colored_text(f"    Welcome, {username} ", 'cyan'))
    print(colored_text("    Unleash the Digital Deluge ", 'yellow'))
    await animated_separator(color='bold_cyan', length=40, animation_char='▓')
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
                    print(colored_text(f"[!] Invalid API_ID in line: {line.strip()}. Skipping account.", 'bold_red'))
    except FileNotFoundError:
        print(colored_text(f"[!] {accounts_file} not found. Create this file with account details.", 'bold_red'))
        print(colored_text("[!] Each line: API_ID,API_HASH,PHONE_NUMBER", 'yellow'))
        return None
    if not accounts:
        print(colored_text("[!] No valid accounts found in accounts.txt.", 'bold_red'))
        return None
    return accounts

async def authorize_account(account):
    """Authorizes a single Telegram account."""
    client = TelegramClient(account['session_name'], account['api_id'], account['api_hash'])
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(account['phone_number'])
            auth_code = input(colored_text(f"[+] Enter authorization code for {account['phone_number']}: ", 'cyan'))
            try:
                await client.sign_in(account['phone_number'], auth_code)
            except SessionPasswordNeededError:
                password = input(colored_text(f"[+] Enter 2FA password for {account['phone_number']}: ", 'cyan'))
                await client.sign_in(password=password)
            print(colored_text(f"[+] Account {account['phone_number']} AUTHORIZED.", 'bold_green'))
        return client
    except Exception as e:
        print(colored_text(f"[!] Authorization failed for account {account['phone_number']}: {e}", 'bold_red'))
        return None

async def authorize_accounts(accounts):
    """Authorizes all accounts concurrently before spamming."""
    print(colored_text("[+] Pre-authorizing all accounts...", 'cyan'))
    auth_tasks = [authorize_account(account) for account in accounts]
    authorized_clients = await asyncio.gather(*auth_tasks)
    valid_clients = [client for client in authorized_clients if client]
    if len(valid_clients) < len(accounts):
        print(colored_text(f"[!] Warning: Only {len(valid_clients)} out of {len(accounts)} accounts authorized successfully.", 'bold_yellow'))
    else:
        print(colored_text(f"[+] All {len(valid_clients)} accounts authorized.", 'bold_green'))
    return valid_clients

async def spam_attack():
    """Main function to orchestrate the spam attack."""
    await welcome_screen()

    accounts = load_accounts()
    if not accounts:
        return

    await loading_animation(message=colored_text("[+] Loading Accounts", 'cyan'), duration=loading_animation_duration)
    print(colored_text(f"[+] Loaded {len(accounts)} accounts.", 'bold_green'))

    authorized_clients = await authorize_accounts(accounts)
    if not authorized_clients:
        print(colored_text("[!] No accounts authorized. Aborting.", 'bold_red'))
        return

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text("     Message Type Selection", 'bold_cyan'), delay=0.01)
    await animated_separator(color='cyan', length=40)
    print(colored_text("  1. Single custom message", 'white'))
    print(colored_text("  2. Multiple custom messages", 'white'))
    print(colored_text("  3. Random messages (custom length)", 'white'))
    print(colored_text("  4. Dynamic messages (from phrases.txt)", 'white'))
    message_type_choice = input(colored_text(colored_text("[+] ", 'cyan') + "Enter choice (1/2/3/4): ", 'white'))
    await animated_separator(color='cyan', length=40)
    print()

    spam_messages = []
    min_random_length = 10
    max_random_length = 50

    if message_type_choice == '1':
        spam_messages.append(input(colored_text(colored_text("[+] ", 'cyan') + "Single custom spam message: ", 'white')))
    elif message_type_choice == '2':
        print(colored_text(colored_text("[+] ", 'cyan') + "Multiple custom spam messages, one per line. Type " + colored_text("'END'", 'bold_yellow') + " when finished:", 'white'))
        while True:
            message_line = input(colored_text(colored_text("[+] ", 'cyan') + "Message line: ", 'white'))
            if message_line.upper() == 'END':
                break
            spam_messages.append(message_line)
        if not spam_messages:
            spam_messages.append("Default spam message - no custom messages provided.")
    elif message_type_choice == '3':
        print(colored_text(colored_text("[+] ", 'cyan') + "Spamming with random messages (custom length).", 'white'))
        min_random_length = int(input(colored_text(colored_text("[+] ", 'cyan') + "Min random message length (default 10): ", 'white')) or min_random_length)
        max_random_length = int(input(colored_text(colored_text("[+] ", 'cyan') + "Max random message length (default 50): ", 'white')) or max_random_length)
    elif message_type_choice == '4':
        print(colored_text(colored_text("[+] ", 'cyan') + "Spamming with dynamic messages from phrases.txt.", 'white'))
        if not os.path.exists("phrases.txt"):
            print(colored_text(colored_text("[!] ", 'bold_red') + "phrases.txt not found. Create in script directory.", 'yellow'))
            print(colored_text(colored_text("[!] ", 'bold_red') + "Each line in phrases.txt is a phrase.", 'yellow'))
            return
    else:
        print(colored_text(colored_text("[!] ", 'bold_red') + "Invalid choice. Defaulting to single custom message.", 'yellow'))
        spam_messages.append(input(colored_text(colored_text("[+] ", 'cyan') + "Single custom spam message: ", 'white')))

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text("       Speed Selection", 'bold_cyan'), delay=0.01)
    await animated_separator(color='cyan', length=40)
    print(colored_text("  1. Normal speed " + colored_text("(recommended)", 'green'), 'white'))
    print(colored_text("  2. Maximum speed " + colored_text("(WARNING: BAN RISK)", 'bold_red'), 'white'))
    speed_choice = input(colored_text(colored_text("[+] ", 'cyan') + "Enter speed choice (1/2): ", 'white'))
    await animated_separator(color='cyan', length=40)
    print()

    if speed_choice == '2':
        delay_between_messages = max_speed_delay
        print(colored_text(colored_text("\n[!!!] WARNING: MAXIMUM SPEED SPAMMING ENABLED. BAN RISK IS EXTREME.", 'bold_red')))
        print(colored_text(colored_text("[!!!] ", 'bold_red') + "Proceed with extreme caution at your own peril.\n", 'yellow'))
    else:
        delay_between_messages = default_delay

    target_entity = input(colored_text(colored_text("[+] ", 'cyan') + "Enter target username/phone number: ", 'white'))
    message_count = int(input(colored_text(colored_text("[+] ", 'cyan') + "Enter number of messages to send: ", 'white')))

    print(colored_text(colored_text("\n[+] ", 'cyan') + "Target acquired. Initiating CONCURRENT multi-account spam attack...", 'bold_cyan'))
    await loading_animation(message=colored_text("[+] Launching Concurrent Multi-Account Torment", 'cyan'), duration=loading_animation_duration)

    # Get target entity before concurrent spam using the first authorized client
    target = await authorized_clients[0].get_entity(target_entity)
    print(colored_text(colored_text("[+] ", 'cyan') + f"Spamming target: {target.title if hasattr(target, 'title') else target.username}...", 'bold_cyan'))

    message_index = 0
    messages_sent_count = 0
    start_time = time.time()

    async def spam_with_account(client, account, messages_per_account):
        """Spams the target with one account."""
        nonlocal messages_sent_count, message_index
        account_sent_count = 0
        for _ in range(messages_per_account):
            try:
                if message_type_choice == '3':
                    current_spam_message = generate_random_message(min_random_length, max_random_length)
                elif message_type_choice == '4':
                    current_spam_message = generate_dynamic_message()
                else:
                    current_spam_message = spam_messages[message_index % len(spam_messages)]

                await client.send_message(target, current_spam_message)
                messages_sent_count += 1
                account_sent_count += 1
                message_index += 1

                estimated_time_remaining_sec = -1 # Cannot reliably estimate remaining time in concurrent mode easily

                await progress_bar(messages_sent_count, message_count * len(authorized_clients), prefix=colored_text(f'[+] Concurrent Spamming', 'cyan'), length=50, base_color='cyan', delay=progress_bar_delay, sent_count=messages_sent_count, estimated_time_remaining="N/A")

                if speed_choice != '2':
                    await asyncio.sleep(delay_between_messages)

            except FloodWaitError as e:
                wait_seconds = e.seconds
                print(colored_text(f"\n[!] Telegram Flood Wait Error (Account: {account['phone_number']}). Waiting {wait_seconds} seconds...", 'bold_yellow'))
                for remaining_time in range(wait_seconds, 0, -1):
                    status_message = colored_text(f" (Waiting due to flood: {remaining_time}s)", 'bold_yellow')
                    print(status_message, end='\r', flush=True)
                    await asyncio.sleep(1)
                print(" " * 50, end='\r', flush=True)
                continue

            except UserBlockedError:
                print(colored_text(f"\n[!] {colored_text(f'Target user blocked account: {account['phone_number']}.', 'bold_red')}", 'red'))
                break

            except PeerFloodError:
                print(colored_text(f"\n[!] {colored_text(f'Peer Flood detected (account {account['phone_number']} rate-limited).', 'bold_yellow')}", 'yellow'))
                print(colored_text(f"[!] {colored_text('Reduce speed or use proxies.', 'bold_red')}", 'yellow'))
                break

            except ChannelPrivateError:
                print(colored_text(f"\n[!] {colored_text(f'Target channel/group private and account {account['phone_number']} not member.', 'bold_red')}", 'red'))
                break

            except Exception as e:
                print(colored_text(f"\n[!] {colored_text(f'General error sending message with account {account['phone_number']}:', 'bold_red')} {e}", 'red'))
                print(colored_text(colored_text("[!] ", 'bold_red') + "Spamming interrupted. Investigate the error.\n", 'yellow'))
                break
        print(colored_text(f"[+] Account {account['phone_number']} deployed {account_sent_count} messages.", 'bold_green'))

    messages_per_account = message_count # Each account sends the full message_count
    spam_tasks = []
    for account, client in zip(accounts, authorized_clients):
        task = asyncio.create_task(spam_with_account(client, account, messages_per_account))
        spam_tasks.append(task)

    await asyncio.gather(*spam_tasks)

    # Serial disconnect of clients
    print(colored_text("[+] Disconnecting clients serially...", 'cyan'))
    for client in authorized_clients:
        if client and client.is_connected():
            await client.disconnect()
    print(colored_text("[+] All clients disconnected.", 'bold_green'))

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text(f"\n[+] Concurrent multi-account spam attack complete (for now). {messages_sent_count} messages deployed. Digital pandemonium unleashed.", 'bold_green'), delay=0.01)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=colored_text("Telegram Spammer - Concurrent Multi-Account Edition", 'bold_cyan'))
    parser.add_argument('--separator_delay', '-sd', type=float, help=colored_text('Separator animation delay (default: 0.01)', 'white'), default=separator_animation_delay)
    parser.add_argument('--progress_delay', '-pd', type=float, help=colored_text('Progress bar delay (default: 0.01)', 'white'), default=progress_bar_delay)
    parser.add_argument('--loading_duration', '-ld', type=float, help=colored_text('Loading animation duration (default: 1.5)', 'white'), default=loading_animation_duration)

    args = parser.parse_args()

    separator_animation_delay = args.separator_delay
    progress_bar_delay = args.progress_delay
    loading_animation_duration = args.loading_duration

    asyncio.run(spam_attack())