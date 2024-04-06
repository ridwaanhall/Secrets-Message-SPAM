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
    message_data = {"id": message_id, "message": message_text*10000}
    
    # Ask if the user wants to send the message multiple times
    send_multiple_times = input("\nDo you want to spam this message? (yes/no): ")
    if send_multiple_times.lower() in ["yes", "y", ""]:
        # If yes, ask how many times to spam
        num_times = input("How many times do you want to spam this message? (Enter a number): ")
        try:
            num_times = int(num_times)
        except ValueError:
            print("Invalid input. Please enter a number.")
            exit()
        
        # Send the message multiple times
        for _ in range(num_times):
            response = client.send_message(message_data)
            print(f"\n{_+1} of {num_times}")
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
