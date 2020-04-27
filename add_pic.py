# Add a picture of a plant to pics folder
# Update db 'has_pic' column to 1 when a picture is added to the pics folder

import sqlite3

import config
import plant_functions

print (plant_functions.current_time())

directory_name = 'pics'

detach_dir = plant_functions.attachments_dir(directory_name)

def add_pic():

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
                    # text = email_parse[1]
                    # email_from = email_parse[2]
                    plant_name = email_parse[3]

                    if checker == 'add pic':
                        plant_functions.delete_emails(id_list,i,mail)

                        conn = sqlite3.connect(config.DB_NAME)
                        conn.execute("UPDATE watering_schedule SET has_pic = 1 WHERE plant_name = '" + plant_name + "'")
                        conn.commit()
                        conn.close()

                        print ('DB has_pic column has been set to 1 for ' + plant_name)

        print ("Done")

    else:
        print ('Mailbox is empty!')


add_pic()