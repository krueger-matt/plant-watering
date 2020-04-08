# This script runs anytime after maintenance.py (I have it run at 10am on weekends and 6pm on weekdays) and sends a text for each plant
# that needs to be watered (based on the need_water field in the db).
# Make sure the TO = [] line is updated with a phone number for the text to be sent to. Each mobile carrier uses a different
# domain after the phone number for email to text.

import time
import os
import sqlite3
import datetime

import plant_functions

print datetime.datetime.now()

# Check which plants need water and send a text for each plant if they need water
def send_text():
    print 'Starting...'

    row = []

    # Checks which plants have a need_water flag set to 1 and then sends one text per plant that needs water
    conn = sqlite3.connect('plants.db')
    cursor = conn.execute("SELECT plant_name FROM watering_schedule WHERE need_water = 1 AND ignore = 0")
    for row in cursor:
        # Create email subject to pass to plant_functions
        email_subject = 'Water ' + row[0]
        # Call plant_functions and pass row and email subject
        plant_functions.email_login(row,email_subject)

    if len(row) == 0:
        print 'No plants need watering'

    conn.close()


send_text()