import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

class truck_and_route:
    def __init__(self, starting_location, destination, truck_type):
        self.starting_location = starting_location
        self.destination = destination
        self.truck_type = truck_type

    def __str__(self):
        return (self.starting_location + ' ' + self.destination + ' ' + self.truck_type)
    
    def get_sl(self):
        return self.starting_location
    
    def get_destination(self):
        return self.destination
    
    def get_tt(self):
        return self.truck_type

def send_notification():
    SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
    flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    print("Enter Full your name:\n")
    in_message = input()
    print("Enter truck found destination\n")
    found_destination = input()
    print("Enter truck found starting location\n")
    found_location = input()
    print("Enter truck found truck style\n")
    truck_type = input()
    message = MIMEText('Hi, this is an automated message being sent to you from '+in_message+'. I am notifying you that a truck you have been searching for has been found.\n Starting Location: '+found_location+'\n Destination: '+found_destination+'\n Truck Type: '+truck_type)
    print("Write an email address to send this message to:\n")
    message['to'] = input()
    message['subject'] = 'Truck Finder 312 Automated Message'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

def parse_routes(routes):
    #This function will parse a long pasted input and file the routes list
    #DO NOT ENTER DUPLICATES ON THE LIST(i.e. check the list for duplicates for each additional element or something)
    #filter out power only equipment types
    one = truck_and_route("Chicago", "Greensboro", "Reefer")
    two = truck_and_route("Riverside", "Silver Grove", "Barge")
    routes.append(one)
    routes.append(two)
    return


def main():
    # Receive some form of pasted text to parse and file into a data structure
    routes = []
    parse_routes(routes) #(doesn't exist yet)
    for route in routes:
        print(route)
    # Launch DAT API instances per element on the list routes
    
    send_notification()
    return

if __name__ == "__main__":
    main()