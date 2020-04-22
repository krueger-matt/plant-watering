# Add a plant via text
# To use, text "Add Plant: plant_name, schedule in days" in that exact syntax. It will automatically create a row in the
# watering_schedule table, populate the current time as last_watered, and 0 for all of the other fields

import sqlite3
import datetime

import config
import plant_functions

print datetime.datetime.now()

directory_name = 'attachments'

detach_dir = plant_functions.attachments_dir(directory_name)

def add_plant():

    email_login = plant_functions.email_login()
    mail = email_login[0]
    mail_ids = email_login[1]

    # If this is true, that means there are emails in the inbox. If not, then no mail!
    if len(mail_ids) > 0:

        conn = sqlite3.connect(config.DB_NAME)

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

                    if checker == 'add plant':

                        print "checker: " + str(checker)

                        if text.startswith('Add Plant:'):
                            start_text = text.find(':') + 2
                            end_text = text.find(',')
                            plant_name = text[start_text:end_text]

                            schedule_in_days = text[end_text + 2:]

                            sql = "INSERT INTO watering_schedule (plant_name, schedule_in_days, last_watered, days_since_last_water, need_water, ignore) VALUES ('" + str(plant_name + "','" + str(schedule_in_days) + "', (SELECT datetime('now','localtime')), 0, 0, 0)")

                            print sql

                            cursor = conn.execute(sql)
                            conn.commit()

                            # Create email subject to pass to plant_functions
                            email_subject = 'Plant Added:'
                            email_body = "Added " + plant_name + " with watering schedule of " + str(schedule_in_days) + " days to plants database!"
                            # Call plant_functions and pass row and email subject
                            plant_functions.send_email(email_subject,email_body)

                        plant_functions.delete_emails(id_list,i,mail)

                    else:
                        print "No add plant emails in inbox"

        conn.close()
        print "Done"

    else:
        print 'Mailbox is empty!'


add_plant()