

import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with your Firebase service account key
cred = credentials.Certificate(r"C:\Users\User\Desktop\disaster management system\templates\disastermanagement-7cf27-firebase-adminsdk-fbsvc-34342354b8.json")  # Replace with your service account key path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://disastermanagement-7cf27-default-rtdb.firebaseio.com/'
})

# Function to extract phone numbers from the Firebase data
# def extract_phone_numbers(data, country_filter=None):
#     phone_numbers = []

#     # Iterate through each citizen's data
#     for citizen_id, citizen_data in data.items():
#         # Optionally filter by Country and State
#         if (country_filter and citizen_data.get('Country') == country_filter):
#             phone_numbers.append(citizen_data.get('Phoneno'))
#         # else:
#         #     # Extract phone number for all citizens if no specific filtering is required
#         #     phone_numbers.append(citizen_data.get('Phoneno'))

#     return phone_numbers

def extract_mail(data, country_filter=None):
    mails = []

    # Iterate through each citizen's data
    for citizen_id, citizen_data in data.items():
        # Optionally filter by Country and State
        if (country_filter and citizen_data.get('Country') == country_filter):
            mails.append(citizen_data.get('Mail'))
        # else:
        #     # Extract phone number for all citizens if no specific filtering is required
        #     mails.append(citizen_data.get('Phoneno'))

    return mails

# Retrieve data from Firebase Realtime Database
ref = db.reference('citizen')  # Reference to the 'citizen' node in Firebase database
snapshot = ref.get()  # Get all data

# if snapshot:
#     # Extract phone numbers based on a specific country and state filter
#     country_filter = "34"  # Example: filter by country
#     state_filter = "desiredState"  # Example: filter by state
#     phone_numbers = extract_phone_numbers(snapshot, country_filter, state_filter)
#     print("Extracted Phone Numbers:", phone_numbers)
# else:
#     print("No data found or unable to retrieve data.")


import requests
import time
from datetime import datetime, timezone, timedelta
# import pywhatkit as kit

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials and details
sender_email = "guptarashmi2703@gmail.com"
password = "xfiy vyog wlri gjij"
# URL of the GeoJSON file
url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'

# Variable to store the last displayed earthquake's timestamp
last_displayed_timestamp = None

# Function to extract the country name from the place
def extract_country(place):
    # Extract the country name after the last comma
    parts = place.split(',')
    return parts[-1].strip() if len(parts) > 1 else None

# Function to check if the earthquake happened today
def is_today(time_stamp):
    # Convert timestamp to timezone-aware datetime in UTC
    earthquake_date = datetime.fromtimestamp(time_stamp / 1000, tz=timezone.utc)
    today = datetime.utcnow().replace(tzinfo=timezone.utc)  # Get the current date in UTC

    # Compare only the date part (year, month, day)
    return earthquake_date.date() == today.date()

# Function to fetch the latest GeoJSON data and process it
def fetch_earthquakes():
    global last_displayed_timestamp
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()  # Parse the response JSON

        features = data['features']  # Get the earthquake features array

        # Filter the features that occurred today
        today_earthquakes = [feature for feature in features if is_today(feature['properties']['time'])]

        if today_earthquakes:
            # Sort the earthquakes by the timestamp, most recent first
            most_recent_earthquake = max(today_earthquakes, key=lambda x: x['properties']['time'])

            # Get the timestamp of the most recent earthquake
            current_timestamp = most_recent_earthquake['properties']['time']

            # If the timestamp hasn't changed, do not display the earthquake again
            if current_timestamp == last_displayed_timestamp:
                return

            # Update the last displayed timestamp
            last_displayed_timestamp = current_timestamp

            # Extract and print the most recent earthquake's details
            place = most_recent_earthquake['properties']['place']  # Get the location of the earthquake
            country = extract_country(place)  # Extract the country
            time_stamp = most_recent_earthquake['properties']['time']
            time = datetime.fromtimestamp(time_stamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')  # Convert the timestamp to a readable format
            title = most_recent_earthquake['properties']['title']

            

            dt = datetime.fromtimestamp(time_stamp / 1000, tz=timezone.utc)
            print(f"Most Recent Earthquake:")
            print(f"Time: {time}")
            print(f"Location: {place}")
            print(f"Country: {country}")
            print(f"Title: {title}")
            print("--------------------------------")
            # ist_offset = timedelta(hours=5, minutes=30)

            # dt_utc = datetime.fromtimestamp(time_stamp / 1000, tz=timezone.utc)

            # # Convert the UTC datetime to IST by adding the offset
            # dt_ist = dt_utc + ist_offset

            # # Convert the IST datetime to a string in the format you want
            # time_ist = dt_ist.strftime('%Y-%m-%d %H:%M:%S')

            # # Print the time in IST
            # print(f"Time in IST: {time_ist}")


            # Create a timedelta object to add 10 minutes
            # new_time = dt_ist + timedelta(minutes=23)

            # # Extract the new hour and minute after adding 10 minutes
            # new_hour = new_time.hour
            # new_minute = new_time.minute
            if snapshot:
                # Extract phone numbers based on a specific country and state filter
                # phone_numbers = extract_phone_numbers(snapshot, country)
                # print("Extracted Phone Numbers:", phone_numbers)

                mails =  extract_mail(snapshot, country)
                print("Extracted Mail:", mails)

                for mail in mails:
                     subject = "Alert"
                     body_plain = title
                     
                     msg = MIMEMultipart()
                     msg['From'] = sender_email
                     msg['To'] = mail
                     msg['Subject'] = subject
                     msg['Reply-To'] = sender_email  # Add a proper reply-to address
                     msg.attach(MIMEText(body_plain, 'plain'))
                     
                    #  try:
                     with smtplib.SMTP('smtp.gmail.com', 587) as server:
                             server.starttls()  # Secure the connection
                             server.login(sender_email, password)  # Login with email and password
                             server.sendmail(sender_email, mail, msg.as_string())  # Send email
                             print("Email sent successfully!")
                    #  except Exception as e:
                        #  print(f"Failed to send email: {e}")

                

                # for phoneno in phone_numbers:
                #     kit.sendwhatmsg('+'+phoneno, 'Alert: '+title, new_hour, new_minute)
            else:
                print("No data found or unable to retrieve data.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GeoJSON data: {e}")

# Set an interval to fetch new data every 30 seconds (30 seconds = 30)
def start_updating(interval=30):
    while True:
        fetch_earthquakes()  # Fetch and display the latest earthquakes
        time.sleep(interval)  # Wait for the specified interval before fetching again

# Start the process with a 30-second interval
start_updating(interval=30)
