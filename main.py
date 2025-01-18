import pandas as pd
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_messages(leads, client, message_text, failed_log_path):
    with open(failed_log_path, "w") as failed_log:
        for index, lead in leads.iterrows():
            name = lead['name']  # Assuming the first column is named 'name'
            phone_number = lead['phone_number']  # Assuming the second column is named 'phone_number'
            try:
                message = client.messages.create(
                    to=phone_number,
                    from_="yournumber",  # Replace with your Twilio phone number
                    body=message_text
                )
                print(f"Message sent to {name} at {phone_number}")
                time.sleep(5)  # Wait for 5 seconds before sending the next message
            except TwilioRestException as e:
                failed_log.write(f"{name},{phone_number},{e}\n")
                print(f"Twilio error when sending to {name} at {phone_number}: {e}")
            except Exception as e:
                failed_log.write(f"{name},{phone_number},{e}\n")
                print(f"General error when sending to {name} at {phone_number}: {e}")

def main():
    leads_csv = r'c:\YOURFILE'  # Replace with your CSV file path
    failed_log_path = 'failed_messages.txt'  # Path to log file for failed messages
    account_sid = ''
    auth_token = ''

    try:
        # Load leads from CSV
        leads = pd.read_csv(leads_csv, usecols=['name', 'phone_number'])
    except FileNotFoundError:
        print(f"CSV file not found: {leads_csv}")
        return
    except pd.errors.ParserError:
        print(f"Error parsing CSV file: {leads_csv}")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    try:
        # Setup Twilio client
        client = Client(account_sid, auth_token)
    except Exception as e:
        print(f"Error setting up Twilio client: {e}")
        return

    # Sending messages
    message_text = "!"
    send_messages(leads, client, message_text, failed_log_path)

    print("All messages attempted. Check 'failed_messages.txt' for any failures.")

if __name__ == "__main__":
    main()
