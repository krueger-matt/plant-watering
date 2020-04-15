# This script runs every 10 minutes. It checks if anyone has emailed a plant name which means they want to know when it should be watered next
# If it finds an email with a plant name, it sends a text back saying when the plant next needs water
# Make sure the TO = [] line is updated with a phone number for the text to be sent to.

import time
import os
import sqlite3
import datetime

import config
import plant_functions

print datetime.datetime.now()

detach_dir = plant_functions.attachments_dir()

# Function to go to Gmail and read emails
# Looks for emails with just a plant name in them
# Sends a text to users with the number of days until that plant needs to be watered
def check_status():

    row = []
    conn = sqlite3.connect('plants.db')

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT plant_name, schedule_in_days - days_since_last_water FROM watering_schedule WHERE ignore = 0")

# Hold query in dictionary
    output = {}

# Add items to dictionary
    for row in cursor:
        output[str(row[0])] = row[1]

# Create list of plant names from 'output' dictionary
    plant_list = output.keys()

    mail = plant_functions.email_login()

    mail.select('inbox')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    # If this is true, that means there are emails in the inbox. If not, then no mail!
    if len(mail_ids) > 0:

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        # Loop through all emails starting with earliest ID and incrementing by 1 to highest email ID
        for i in range(first_email_id,latest_email_id + 1, 1):

            print "i: " + str(i)

            typ, data = mail.fetch(i, '(RFC822)' )

            # Grab email data including from, subject, and time
            for response_part in data:
                if isinstance(response_part, tuple):

                    email_parse = plant_functions.email_parse(detach_dir,response_part)
                    checker = email_parse[0]
                    text = email_parse[1]
                    email_from = email_parse[2]

                    if checker > 0:

                        print "checker: " + str(checker)

                        # This neat trick finds the first instance of a string inside a list
                        # So what we want to do is look if the email attachment has any of our plants in it
                        # Tbis could get dicey if a plant had a very similar name another in the database
                        if any(plant in text for plant in plant_list):

                            # removed_string takes the text variable, which is the email attachment, and removes the ' status' portion in order to get the plant name
                            removed_string = text.find(' status')
                            plant = text[0:removed_string]

                            # status is the number of days until that plant needs to be watered (stored in the output dictionary)
                            status = output.get(plant)

                            # Create email subject to pass to plant_functions
                            email_subject = 'Status:'
                            email_body = "Water " + plant + " in " + str(status) + " days"
                            # Call plant_functions and pass row and email subject
                            plant_functions.send_email(email_subject,email_body,row)

                        elif text.strip().lower() == "all status":
                            email_subject = 'Overall Status:'
                            email_body = "Water:\n" + "".join(" in ".join((str(k),(str(v)+' days' + '\n'))) for k,v in output.items())
                            plant_functions.send_email(email_subject,email_body,row)

                        # Get the mail ID to delete from id_list
                        id_to_delete = id_list[i-1]

                        print 'Email ID list: ' + ', '.join(id_list)

                        print 'Email ID to delete: ' + str(id_to_delete)

                        # Delete the email
                        mail.store(str(id_to_delete), '+X-GM-LABELS', '\\Trash')
                        print 'Email deleted'

                    else:
                        print "checker should be -1. Is it? checker: " + str(checker)

        conn.close()
        print "Done"

    else:
        print 'Mailbox is empty!'


check_status()