# This script runs every hour and checks the Gmail account to see if any plants have been watered.
# If a plant was watered, it updates the db fields:
    # last_watered = now
    # days_since_last_water = 0
    # need_water = 0
# It knows a plant was watered if the user who got the text sends a reply with "Plant Name watered" in that exact syntax.
# If it finds an email saying a plant was watered, it will send a text confirming the action. This is useful
# for situations when multiple people are getting the plant watering texts.
# Make sure the TO = [] line is updated with a phone number for the text to be sent to.

import time
import os
import sqlite3
import datetime

import config
import plant_functions

print datetime.datetime.now()

FROM_EMAIL  = config.FROM_EMAIL
FROM_PWD    = config.FROM_PWD
SMTP_SERVER = config.SMTP_SERVER
SMTP_PORT   = config.SMTP_PORT

detach_dir = plant_functions.attachments_dir()

# Function to go to Gmail and read emails. Checks to find ones with text that = 'Watered'
# If there is a text saying "Plant Name watered" then update datebase column last_watered with current datetime
# After database is updated, send text confirming to all users that the plant has been watered
# Update score_keeper table with plant_id, email, and date everytime a plant is successfully watered. This can be used
# to gamify the plant watering app!
def read_email_from_gmail():

    row = []
    conn = sqlite3.connect('plants.db')
    cursor = conn.execute("SELECT plant_name FROM watering_schedule WHERE need_water = 1 AND ignore = 0")

    mail = plant_functions.email_login()

    mail.select('inbox')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]


    # If this is true, that means there are emails in the inbox. If not, then no mail!
    if len(mail_ids) > 0:

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        # Loop through all of the plant_names that the SQL query above pulled (all plants where need_water = 1)
        for row in cursor:

            print 'Looking for ' + str(row[0])

            # Loop through all emails starting with earliest ID and incrementing by 1 to highest email ID
            for i in range(first_email_id,latest_email_id + 1, 1):

                print "Email ID: " + str(i)

                typ, data = mail.fetch(i, '(RFC822)' )

                # Grab email data including from, subject, and time
                for response_part in data:
                    if isinstance(response_part, tuple):

                        email_parse = plant_functions.email_parse(detach_dir,response_part)
                        checker = email_parse[0]
                        text = email_parse[1]
                        email_from = email_parse[2]

                        if checker > 0:

                            print "Checker: " + str(checker)

                            # text.strip() to remove leading and especially trailing whitespace
                            if text.strip() == row[0] + " watered":
                                conn.execute("update watering_schedule set last_watered = datetime('now'), days_since_last_water = 0, need_water = 0 where plant_name = '" + row[0] + "'")
                                conn.commit()

                                plant_name = row[0]

                                print plant_name + ' record updated'

                                # New cursor to run query to get plant_id
                                plant_id_cursor = conn.execute("select id from watering_schedule where plant_name = '" + plant_name + "'")

                                # Get actual plant_id from the cursor
                                for plant in plant_id_cursor:
                                    plant_id = plant[0]

                                print plant_id

                                score_keeper_sql = ("insert into score_keeper (plant_id,email,timestamp) values(" + str(plant_id) + ",'" + email_from + "',date('now'))")
                                print score_keeper_sql

                                # Insert plant_id and email into score_keeper table
                                conn.execute(score_keeper_sql)
                                conn.commit()

                                # Create email subject to pass to plant_functions
                                email_subject = row[0] + ' watered'
                                # Call plant_functions and pass row and email subject
                                plant_functions.send_email(email_subject,row)

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


read_email_from_gmail()