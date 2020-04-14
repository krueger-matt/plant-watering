# This checks if anyone has texted Get Score and responds with the current score from the score_keeper table

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

def get_score():

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

                    if checker >= 0:

                        print "checker: " + str(checker)

                        if text.strip().lower() == "get score":

                            # Create email subject to pass to plant_functions
                            email_subject = plant_functions.get_overall_score()

                            # Call plant_functions and pass row and email subject
                            plant_functions.send_email(email_subject)

                            # Get the mail ID to delete from id_list
                            id_to_delete = id_list[i-1]

                            print 'Email ID list: ' + ', '.join(id_list)

                            print 'Email ID to delete: ' + str(id_to_delete)

                            # Delete the email
                            mail.store(str(id_to_delete), '+X-GM-LABELS', '\\Trash')
                            print 'Email deleted'

                    else:
                        print "checker should be -1. Is it? checker: " + str(checker)

        print "Done"

    else:
        print 'Mailbox is empty!'


get_score()