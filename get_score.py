# This checks if anyone has texted Get Score and responds with the current score from the score_keeper table

import sqlite3

import config
import plant_functions

print (plant_functions.current_time())

directory_name = 'attachments'

detach_dir = plant_functions.attachments_dir(directory_name)

def get_score():

    email_login = plant_functions.email_login()
    mail = email_login[0]
    mail_ids = email_login[1]

    # If this is true, that means there are emails in the inbox. If not, then no mail!
    if len(mail_ids) > 0:

        id_list = mail_ids.decode().split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        # Loop through all emails starting with earliest ID and incrementing by 1 to highest email ID
        for i in range(first_email_id,latest_email_id + 1, 1):

            print ("i: " + str(i))

            typ, data = mail.fetch(str(i), '(RFC822)' )

            # Grab email data including from, subject, and time
            for response_part in data:
                if isinstance(response_part, tuple):

                    email_parse = plant_functions.email_parse(detach_dir,response_part,directory_name)
                    checker = email_parse[0]
                    text = email_parse[1]
                    email_from = email_parse[2]

                    if checker == 'get score':

                        print ("checker: " + str(checker))

                        if text.strip().lower() == "get score":

                            # Create email subject to pass to plant_functions
                            email_body = plant_functions.get_overall_score()
                            email_body = str(email_body)
                            email_subject = "Overall score:"

                            # Call plant_functions and pass row and email subject
                            plant_functions.send_email(email_subject,email_body)

                            plant_functions.delete_emails(id_list,i,mail)

                    else:
                        print ("No get score emails in inbox")

        print ("Done")

    else:
        print ('Mailbox is empty!')


get_score()