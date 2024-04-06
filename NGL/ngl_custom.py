import os
from dotenv import load_dotenv
import requests
from fake_useragent import UserAgent
import random
import string
import time


class RequestSender:
    def __init__(self, url):
        self.url = url

    def send_request(self, username, question, deviceId, gameSlug='', referrer=''):
        ua = UserAgent()
        headers = self._generate_headers(username)
        data = {
            'username': username,
            'question': question,
            'deviceId': deviceId,
            'gameSlug': gameSlug,
            'referrer': referrer
        }
        response = requests.post(self.url, headers=headers, data=data)
        return response

    def send_request_with_retry(self, username, question, deviceId, gameSlug='', referrer='', max_retries=3):
        retries = 0
        while retries < max_retries:
            response = self.send_request(username, question, deviceId, gameSlug, referrer)
            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get('Retry-After', 10))  # Default to waiting 10 seconds
                for countdown in range(retry_after, 0, -1):
                    print(f'\rRetrying in {countdown} seconds...', end='', flush=True)
                    time.sleep(1)
                print()  # Print newline after countdown completes
                retries += 1
            elif response.status_code == 200:  # Success
                return response
            else:
                print(f"Unexpected error: {response.status_code} - {response.reason}")
                exit()
                return response
        print("Max retries reached. Failed to send request.")
        return None

    def _generate_headers(self, username):
        sec_ch_ua = [
            '"Microsoft Edge";v="123"',
            '"Not:A-Brand";v="8"',
            '"Chromium";v="123"'
        ]
        sec_ch_ua_mobile = ['?0', '?1']
        sec_ch_ua_platform = ['"Windows"', '"Linux"', '"Macintosh"', '"Android"', '"iOS"']

        return {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Dnt': '1',
            'Referer': f'https://ngl.link/{username}',
            'Sec-Ch-Ua': random.choice(sec_ch_ua),
            'Sec-Ch-Ua-Mobile': random.choice(sec_ch_ua_mobile),
            'Sec-Ch-Ua-Platform': random.choice(sec_ch_ua_platform),
            'User-Agent': UserAgent().random
        }


class deviceIDGenerator:
    def __init__(self):
        pass

    def generate_deviceId(self):
        random_deviceId = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_deviceId += '-'
        random_deviceId += ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        random_deviceId += '-'
        random_deviceId += ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        random_deviceId += '-'
        random_deviceId += ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        random_deviceId += '-'
        random_deviceId += ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return random_deviceId


class GameSlugGenerator:
    def __init__(self):
        self.game_slugs = [
            "",
            "confessions",
            "3words",
            "tbh",
            "shipme",
            "yourcrush",
            "cancelled",
            "dealbreaker"
        ]

    def generate_game_slug(self):
        return random.choice(self.game_slugs)


class GameSlugSelector:
    def __init__(self):
        self.game_slugs = {
            "1": "",
            "2": "confessions",
            "3": "3words",
            "4": "tbh",
            "5": "shipme",
            "6": "yourcrush",
            "7": "cancelled",
            "8": "dealbreaker"
        }

    def select_game_slug(self):
        print("\nSelect a game slug:")
        for key, value in self.game_slugs.items():
            print(f"{key}: {value}")

        while True:
            choice = input("\nEnter your choice (1-8): ")
            if choice in self.game_slugs.keys():
                return self.game_slugs[choice]
            else:
                print("Invalid choice. Please enter a number between 1 and 8. - ")


if __name__ == "__main__":
    load_dotenv()

    url = os.getenv("URL_NGL")
    request_sender = RequestSender(url)
    game_slug_generator = GameSlugGenerator()
    game_slug_selector = GameSlugSelector()

    while True:
        username = input("Enter username target (required): ")
        if username.strip():  # Checks if the input is not empty after stripping whitespace
            break
        else:
            print("Username is required. Please enter a valid username.")

    message = input("Enter your message: ")

    spam_choice = input("\nDo you want to spam? (yes/no): ").lower()
    if spam_choice == "yes" or spam_choice == "" or spam_choice == "y":
        while True:
            spam_count_input = input("How many times do you want to spam?: ").strip()
            if spam_count_input.isdigit():
                spam_count = int(spam_count_input)
                break
            else:
                print("Please enter a valid number for the spam count.")
        
        for _ in range(spam_count):
            gameSlug = game_slug_generator.generate_game_slug()
            deviceId = deviceIDGenerator().generate_deviceId()
            referrer = ""
            response = request_sender.send_request_with_retry(username, message, deviceId, gameSlug, referrer)
            print(f'\n{_ + 1} of {spam_count}')
            print(f'{response.status_code} {response.reason} = {response.text}')
            print(f'gameSlug: {gameSlug}')
            print(f'username: {username}')
            print(f'message : {message}')
    else:
        gameSlug = game_slug_selector.select_game_slug()
        deviceId = os.getenv("DEVICE_ID")
        referrer = ""

        response = request_sender.send_request_with_retry(username, message, deviceId, gameSlug, referrer)
        print(f'gameSlug: {gameSlug}')
        print(f'message : {message}')
        print(f'{response.status_code} {response.reason} = {response.text}')
