import os
import requests
from fake_useragent import UserAgent
from dotenv import load_dotenv

class SecretAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_message(self, message_data):
        url = f"{self.base_url}/sendmsg"
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": UserAgent().random
        }
        response = requests.post(url, headers=headers, json=message_data)
        return response

# Load environment variables from .env file
load_dotenv()

# Example usage
if __name__ == "__main__":
    # Retrieve base URL from environment variable
    base_url = os.getenv("URL_SECRETO")
    
    # Create SecretAPIClient instance
    client = SecretAPIClient(base_url)
    
    # Take input for id and message
    message_id = input("Enter message id: ")
    message_text = input("Enter message text: ")
    
    # Construct message data
    message_data = {"id": message_id, "message": message_text*1000}
    
    # Ask if the user wants to send the message multiple times
    send_multiple_times = input("\nDo you want to spam this message? (yes/no): ")
    if send_multiple_times.lower() in ["yes", "y", ""]:
        while True:
            spam_count = input("How many times do you want to spam? (default: 10000): ").strip()
            if spam_count.isdigit():
                spam_count = int(spam_count)
                break
            elif spam_count == "":
                spam_count = 10000
                break
            else:
                print("Please enter a valid number for the spam count.")
        
        # Send the message multiple times
        for _ in range(spam_count):
            response = client.send_message(message_data)
            print(f"\n{_+1} of {spam_count}")
            print("Response Code:", response.status_code)
            print("Response Text:", response.text)
            print("ID           :", message_id)
            print("Message text :", message_text)
    else:
        # If no, send the message once
        response = client.send_message(message_data)
        print("\nResponse Code:", response.status_code)
        print("Response Text:", response.text)
        print("Message text :", message_text)
