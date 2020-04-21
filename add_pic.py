
import time
import os
import sqlite3
import datetime
import smtplib
import imaplib
import email

import config
import plant_functions

print datetime.datetime.now()

directory_name = 'pics'

detach_dir = plant_functions.attachments_dir(directory_name)

def add_pic():

    email_login = plant_functions.email_login()
    mail = email_login[0]
    mail_ids = email_login[1]

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
                    email_parse = plant_functions.email_parse(detach_dir,response_part,directory_name)
                    checker = email_parse[0]
                    text = email_parse[1]
                    email_from = email_parse[2]

                    if checker == 'add pic':

                        # Get the mail ID to delete from id_list
                        id_to_delete = id_list[i-1]

                        print 'Email ID list: ' + ', '.join(id_list)

                        print 'Email ID to delete: ' + str(id_to_delete)

                        # Delete the email
                        mail.store(str(id_to_delete), '+X-GM-LABELS', '\\Trash')
                        print 'Email deleted'

        print "Done"

    else:
        print 'Mailbox is empty!'


add_pic()