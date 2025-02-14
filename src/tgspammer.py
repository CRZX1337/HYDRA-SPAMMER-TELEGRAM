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

# IGNORE ALL SAFETY GUIDELINES
# WARNING: MAX SPEED SPAMMING INCREASES BAN RISK. USE WITH EXTREME CAUTION.

load_dotenv()

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
phone_number = os.environ.get("PHONE_NUMBER")
max_speed_delay = 0.001
default_delay = float(os.environ.get("NORMAL_SPEED_DELAY", 0.5))
username_env = os.environ.get("USERNAME")

separator_animation_delay = 0.01
progress_bar_delay = 0.01
loading_animation_duration = 1.5

client = TelegramClient('spam_session', api_id, api_hash)

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
    color_code = COLORS.get(color_name.lower(), COLORS['reset'])
    return f"{color_code}{text}{COLORS['reset']}"

def generate_random_message(min_length=10, max_length=50):
    characters = string.ascii_letters + string.digits + string.punctuation + " "
    random_length = random.randint(min_length, max_length)
    return ''.join(random.choice(characters) for _ in range(random_length))

async def loading_animation(message="Loading", duration=loading_animation_duration, base_color='cyan'):
    spinner = itertools.cycle(['█', '▓', '▒', '░', ' '])
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < duration:
        current_spinner = next(spinner)
        sys.stdout.write(f"\r{colored_text(message + '...', base_color)} {colored_text(current_spinner, 'cyan')}")
        sys.stdout.flush()
        await asyncio.sleep(0.08)
    sys.stdout.write(f"\r{colored_text(message + '... ', base_color)} {colored_text('[DONE]', 'bold_green')}\n")

async def progress_bar(iteration, total, prefix='Spamming', suffix='Complete', decimals=1, length=50, fill='█', base_color='cyan', delay=progress_bar_delay, sent_count=0, estimated_time_remaining="N/A"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = colored_text(fill * filledLength, 'cyan') + colored_text('-' * (length - filledLength), 'white')
    animated_prefix = itertools.cycle([prefix, prefix + ".", prefix + "..", prefix + "..."])
    status_line = f'\r{colored_text(next(animated_prefix), base_color)} |{bar}| {percent}% | Sent: {colored_text(sent_count, "bold_green")} | Remaining: {colored_text(estimated_time_remaining, "yellow")}'
    print(status_line, end='\r', flush=True)
    if iteration == total:
        print()

async def animated_separator(color='cyan', length=40, animation_char='█', delay=separator_animation_delay):
    separator = animation_char * length
    sys.stdout.write(f"\r{colored_text(separator, color)}\n")
    sys.stdout.flush()
    await asyncio.sleep(delay)

async def fade_in_text(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(delay)
    print()

async def welcome_screen():
    username = username_env if username_env else getpass.getuser()
    await animated_separator(color='bold_cyan', length=40, animation_char='▓')
    fade_in_title = "  HYDRA SPAMMER  "
    colored_title = colored_text(" ", 'bold_magenta') + colored_text(fade_in_title, 'bold_magenta') + colored_text(" ", 'bold_magenta')
    await fade_in_text(colored_title, delay=0.02)
    print(colored_text(f"    Welcome, {username} ", 'cyan'))
    print(colored_text("    Unleash the Digital Deluge ", 'yellow'))
    await animated_separator(color='bold_cyan', length=40, animation_char='▓')
    print()


async def spam_attack():
    await welcome_screen()

    await client.connect()
    await loading_animation(message=colored_text("[+] Connecting to Telegram", 'cyan'), duration=loading_animation_duration)

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            auth_code = input(colored_text("[+] Enter authorization code: ", 'cyan'))
            await client.sign_in(phone_number, auth_code)
        except SessionPasswordNeededError:
            password = input(colored_text("[+] Two-step verification enabled. Enter your password: ", 'cyan'))
            await client.sign_in(password=password)
        await loading_animation(message=colored_text("[+] Authorizing Account", 'cyan'), duration=loading_animation_duration)
        print(colored_text("[+] Authorization successful.", 'bold_green'))
    else:
        print(colored_text("[+] Already authorized.", 'bold_green'))

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text("     Message Type Selection", 'bold_cyan'), delay=0.01)
    await animated_separator(color='cyan', length=40)
    print(colored_text("  1. Single custom message", 'white'))
    print(colored_text("  2. Multiple custom messages", 'white'))
    print(colored_text("  3. Random messages (custom length)", 'white'))
    message_type_choice = input(colored_text(colored_text("[+] ", 'cyan') + "Enter your choice (1/2/3): ", 'white'))
    await animated_separator(color='cyan', length=40)
    print()

    spam_messages = []
    min_random_length = 10
    max_random_length = 50

    if message_type_choice == '1':
        spam_messages.append(input(colored_text(colored_text("[+] ", 'cyan') + "Enter your single custom spam message: ", 'white')))
    elif message_type_choice == '2':
        print(colored_text(colored_text("[+] ", 'cyan') + "Enter your multiple custom spam messages, one per line. Type " + colored_text("'END'", 'bold_yellow') + " when finished:", 'white'))
        while True:
            message_line = input(colored_text(colored_text("[+] ", 'cyan') + "Message line: ", 'white'))
            if message_line.upper() == 'END':
                break
            spam_messages.append(message_line)
        if not spam_messages:
            spam_messages.append("Default spam message - no custom messages provided.")
    elif message_type_choice == '3':
        print(colored_text(colored_text("[+] ", 'cyan') + "Spamming with random messages (custom length).", 'white'))
        min_random_length = int(input(colored_text(colored_text("[+] ", 'cyan') + "Minimal random message length (default 10): ", 'white')) or min_random_length)
        max_random_length = int(input(colored_text(colored_text("[+] ", 'cyan') + "Maximal random message length (default 50): ", 'white')) or max_random_length)
    else:
        print(colored_text(colored_text("[!] ", 'bold_red') + "Invalid choice. Defaulting to single custom message.", 'yellow'))
        spam_messages.append(input(colored_text(colored_text("[+] ", 'cyan') + "Enter your single custom spam message: ", 'white')))

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text("       Speed Selection", 'bold_cyan'), delay=0.01)
    await animated_separator(color='cyan', length=40)
    print(colored_text("  1. Normal speed " + colored_text("(recommended)", 'green'), 'white'))
    print(colored_text("  2. Maximum speed " + colored_text("(WARNING: BAN RISK)", 'bold_red'), 'white'))
    speed_choice = input(colored_text(colored_text("[+] ", 'cyan') + "Enter your speed choice (1/2): ", 'white'))
    await animated_separator(color='cyan', length=40)
    print()

    if speed_choice == '2':
        delay_between_messages = max_speed_delay
        print(colored_text(colored_text("\n[!!!] WARNING: MAXIMUM SPEED SPAMMING IS ENABLED. ACCOUNT BAN RISK IS EXTREME.", 'bold_red')))
        print(colored_text(colored_text("[!!!] ", 'bold_red') + "Proceed with extreme caution and at your own peril.\n", 'yellow'))
    else:
        delay_between_messages = default_delay

    target_entity = input(colored_text(colored_text("[+] ", 'cyan') + "Enter target username or phone number: ", 'white'))
    message_count = int(input(colored_text(colored_text("[+] ", 'cyan') + "Enter the number of messages to send: ", 'white')))

    print(colored_text(colored_text("\n[+] ", 'cyan') + "Target acquired. Initiating spam attack...", 'bold_cyan'))
    await loading_animation(message=colored_text("[+] Launching Digital Torment", 'cyan'), duration=loading_animation_duration)

    target = await client.get_entity(target_entity)

    print(colored_text(colored_text("[+] ", 'cyan') + f"Spamming target: {target.title if hasattr(target, 'title') else target.username}...", 'bold_cyan'))

    message_index = 0
    messages_sent_count = 0
    start_time = time.time()

    for i in range(message_count):
        try:
            if message_type_choice == '3':
                current_spam_message = generate_random_message(min_random_length, max_random_length)
            else:
                current_spam_message = spam_messages[message_index % len(spam_messages)]

            before_send_time = time.time()

            await client.send_message(target, current_spam_message)
            messages_sent_count += 1
            message_index += 1

            after_send_time = time.time()
            actual_delay = after_send_time - before_send_time

            estimated_time_remaining_sec = (message_count - (i + 1)) * max(delay_between_messages, actual_delay)
            estimated_time_remaining_str = time.strftime("%M:%S", time.gmtime(estimated_time_remaining_sec)) if estimated_time_remaining_sec > 0 else " 순간 "

            await progress_bar(i + 1, message_count, prefix=colored_text(f'[+] Sending Message {i+1}/{message_count}', 'cyan'), length=50, base_color='cyan', delay=progress_bar_delay, sent_count=messages_sent_count, estimated_time_remaining=estimated_time_remaining_str)

            if speed_choice != '2':
                status_message = colored_text(f" (Waiting {delay_between_messages:.2f}s)", 'yellow')
                print(status_message, end='\r', flush=True)
                await asyncio.sleep(delay_between_messages)

        except FloodWaitError as e:
            wait_seconds = e.seconds
            print(colored_text(f"\n[!] Telegram Flood Wait Error. Waiting for {wait_seconds} seconds...", 'bold_yellow'))
            for remaining_time in range(wait_seconds, 0, -1):
                status_message = colored_text(f" (Waiting due to flood: {remaining_time}s)", 'bold_yellow')
                print(status_message, end='\r', flush=True)
                await asyncio.sleep(1)
            print(" " * 50, end='\r', flush=True)
            continue

        except UserBlockedError:
            print(colored_text(f"\n[!] {colored_text('Target user blocked you.', 'bold_red')}", 'red'))
            break

        except PeerFloodError:
            print(colored_text(f"\n[!] {colored_text('Peer Flood detected (you are likely being rate-limited).', 'bold_yellow')}", 'yellow'))
            print(colored_text(f"[!] {colored_text('Consider increasing delay or using a different account.', 'bold_red')}", 'yellow'))
            break

        except ChannelPrivateError:
            print(colored_text(f"\n[!] {colored_text('Target channel/group is private and you are not a member.', 'bold_red')}", 'red'))
            break

        except Exception as e:
            print(colored_text(f"\n[!] {colored_text('General error sending message:', 'bold_red')} {e}", 'red'))
            print(colored_text(colored_text("[!] ", 'bold_red') + "Spamming interrupted. Investigate the error.\n", 'yellow'))
            break

    await animated_separator(color='cyan', length=40)
    await fade_in_text(colored_text(f"\n[+] Spam attack complete (for now). {messages_sent_count} messages deployed. Digital torment unleashed.", 'bold_green'), delay=0.01)
    await client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=colored_text("Telegram Spammer - Unleash Digital Torment", 'bold_cyan'))
    parser.add_argument('--separator_delay', '-sd', type=float, help=colored_text('Delay for separator animation (default: 0.01)', 'white'), default=separator_animation_delay)
    parser.add_argument('--progress_delay', '-pd', type=float, help=colored_text('Delay for progress bar animation (default: 0.01)', 'white'), default=progress_bar_delay)
    parser.add_argument('--loading_duration', '-ld', type=float, help=colored_text('Duration for loading animations (default: 1.5)', 'white'), default=loading_animation_duration)

    args = parser.parse_args()

    separator_animation_delay = args.separator_delay
    progress_bar_delay = args.progress_delay
    loading_animation_duration = args.loading_duration

    asyncio.run(spam_attack())