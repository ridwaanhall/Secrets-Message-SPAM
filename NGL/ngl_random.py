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

class MessageGenerator:
    def __init__(self):
        self.generic_messages = [
            "Hey there! Just wanted to drop a quick message to say hi and see how you're doing. Hope you're having a great day! 😊",
            "Hi friend! Sending some positive vibes your way. Hope you're doing well!",
            "Hey buddy! Remember, you're awesome and capable of achieving anything you set your mind to! 💪",
            "Hello! Just checking in to see how you're doing. Let me know if there's anything I can do to support you!",
            "Hi! Wishing you a fantastic day filled with joy and laughter. Keep shining bright! ✨",
            "Hey! Hope your day is as amazing as you are! 😄",
            "Hi there! Just wanted to remind you that you're appreciated and valued. Keep being awesome!",
            "Hey friend! Just dropping by to say hello and spread some positivity your way. Have a wonderful day!",
            "Hello! Sending you lots of love and good vibes. You've got this!",
            "Hi! Remember, every challenge you face is an opportunity to grow stronger. Keep pushing forward!",
            "Hey there! Just wanted to send a quick virtual hug your way. You're not alone, and I'm here for you!",
            "Hi friend! Hope your day is filled with laughter, love, and all the good things in life. You deserve it!"
        ]
        
        self.messages_hacker = [
            "Initiating secure connection. Your digital presence is attracting attention. Stay vigilant. - ShadowCipher",
            "Warning: Unusual activity detected in your online behavior. Exercise caution. - DarkNetOp",
            "Cipher protocol activated. Your online actions have drawn scrutiny. Maintain discretion. - GhostHacker",
            "Alert: Anomaly detected in network traffic. You may be under surveillance. - StealthByte",
            "Security breach alert: Your digital footprint is being monitored. Take evasive action. - PhantomByte",
            "Caution: Digital surveillance detected. Your activities are being watched closely. - CyberPhantom",
            "Intrusion warning: Your online presence is under scrutiny. Stay under the radar. - CryptoGhost",
            "Encryption compromised. Your digital identity may be at risk. Take precautions. - ShadowCipher",
            "Attention: Suspicious network activity detected. Exercise heightened security measures. - DarkNetOp",
            "Security protocol breached. Your digital security may have been compromised. - GhostHacker",
            "Warning: Abnormal data flow detected in your network. Stay alert. - StealthByte",
            "Code red: Unauthorized access detected. Your online security is under threat. - PhantomByte",
            "Initiating secure transmission. Your digital activities have attracted attention. Stay covert. - CyberPhantom",
            "Caution: Anomalies detected in network traffic. Proceed with caution. - CryptoGhost",
            "Alert: Cipher protocol engaged. Your online presence may be compromised. - ShadowCipher",
            "Security breach detected. Your digital identity is vulnerable. Take action. - DarkNetOp",
            "Warning: Digital surveillance in progress. Maintain operational security. - GhostHacker",
            "Attention: Unusual patterns detected in your online behavior. Stay under the radar. - StealthByte",
            "Intrusion alert: Your online activities are being monitored. Stay low-key. - PhantomByte",
            "Encryption compromised. Your digital security may be compromised. Take evasive action. - CyberPhantom",
            "Alert: Suspicious network activity detected. Exercise caution in your online interactions. - CryptoGhost",
            "Security protocol breached. Your digital footprint is attracting unwanted attention. - ShadowCipher",
            "Code red: Unauthorized access detected. Take measures to protect your online security. - DarkNetOp",
            "Initiating secure communication. Your digital presence is under scrutiny. Maintain discretion. - GhostHacker",
            "Caution: Abnormal data flow detected. Your online activities may be compromised. - StealthByte",
            "Alert: Cipher protocol activated. Your digital security is at risk. Take precautions. - PhantomByte",
            "Security breach detected. Your digital privacy may be compromised. Take evasive action. - CyberPhantom",
            "Warning: Digital surveillance detected. Exercise caution in your online interactions. - CryptoGhost",
            "Attention: Unusual activity detected in your network. Stay alert. - ShadowCipher",
            "Intrusion warning: Your digital footprint has been noticed. Stay under the radar. - DarkNetOp",
            "Encryption compromised. Your online security may be compromised. Take action. - GhostHacker",
            "Alert: Suspicious network activity detected. Proceed with caution in your online activities. - StealthByte",
            "Security protocol breached. Your digital identity is vulnerable. Take evasive action. - PhantomByte",
            "Code red: Unauthorized access detected. Exercise caution in your digital interactions. - CyberPhantom",
            "Initiating secure transmission. Your digital presence is under surveillance. Stay covert. - CryptoGhost",
            "Caution: Anomalies detected in network traffic. Maintain operational security. - ShadowCipher",
            "Alert: Cipher protocol engaged. Your digital privacy may be compromised. - DarkNetOp",
            "Security breach detected. Your online activities are being monitored. Take action. - GhostHacker",
            "Warning: Digital surveillance in progress. Stay low-key in your online interactions. - StealthByte",
            "Attention: Unusual patterns detected in your online behavior. Exercise caution. - PhantomByte",
            "Intrusion alert: Your digital security may be compromised. Stay vigilant. - CyberPhantom"
        ]

    def generate_message(self):
        if random.random() < 1:
            return random.choice(self.messages_hacker)
        else:
            return random.choice(self.generic_messages)

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
    message_generator = MessageGenerator()
    game_slug_generator = GameSlugGenerator()
    game_slug_selector = GameSlugSelector()

    username = input("Enter target username: ")
    spam_choice = input("Do you want to spam? (yes/no): ").lower()
    if spam_choice == "yes" or spam_choice == "" or spam_choice == "y":
        while True:
            spam_count_input = input("How many times do you want to spam?: ").strip()
            if spam_count_input.isdigit():
                spam_count = int(spam_count_input)
                break
            else:
                print("Please enter a valid number for the spam count.")
        for _ in range(spam_count):
            message = message_generator.generate_message()  
            gameSlug = game_slug_generator.generate_game_slug()
            deviceId = deviceIDGenerator().generate_deviceId()
            referrer = ""
            response = request_sender.send_request_with_retry(username, message, deviceId, gameSlug, referrer)
            print(f'\n{_ + 1} of {spam_count}')
            print(f'gameSlug: {gameSlug}')
            print(f'message : {message}')
            print(f'{response.status_code}: {response.reason} = {response.text}')
    else:
        message = input("Enter your message: ")
        gameSlug = game_slug_selector.select_game_slug()
        deviceId = os.getenv("DEVICE_ID")
        referrer = ""  

        response = request_sender.send_request_with_retry(username, message, deviceId, gameSlug, referrer)
        print(f'{response.status_code}: {response.reason} = {response.text}')
        print(f'gameSlug: {gameSlug}')
        print(f'message : {message}')
