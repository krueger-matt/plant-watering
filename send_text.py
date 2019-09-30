# This script runs anytime after maintenance.py (I have it run at 10am on weekends and 6pm on weekdays) and sends a text for each plant
# that needs to be watered (based on the need_water field in the db).
# Make sure the TO = [] line is updated with a phone number for the text to be sent to. Each mobile carrier uses a different
# domain after the phone number for email to text.

import smtplib
import time
import imaplib
import email as emaily
import os
import sqlite3
import datetime

print datetime.datetime.now()

FROM_EMAIL  = os.environ.get('FROM_EMAIL')  # Environment variable called FROM_EMAIL set to email address used
FROM_PWD    = os.environ.get('FROM_PWD')    # Environment variable called FROM_PWD set to email password
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# Check which palnts need water and send a text for each plant if they need water
def send_text():
    print 'Starting...'

    row = []

    # Checks which plants have a need_water flag set to 1 and then sends one text per plant that needs water
    conn = sqlite3.connect('plants.db')
    cursor = conn.execute("SELECT plant_name FROM watering_schedule where need_water = 1")
    for row in cursor:
        TO = [] # Phone number goes here as a string
        SUBJECT = 'Water ' + row[0]
        email = SUBJECT
        print SUBJECT

        # Prepare actual message
        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM_EMAIL, ", ".join(TO), SUBJECT, email)

        # Send the mail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(FROM_EMAIL, FROM_PWD)
        server.sendmail(FROM_EMAIL, TO, message)
        server.quit()
        print 'Text sent'
        print ''

    if len(row) == 0:
        print 'No plants need watering'

    conn.close()


send_text()