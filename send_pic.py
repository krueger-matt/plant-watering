# Send a picture of a requested plant to user

import sqlite3
import os

import config
import plant_functions

directory_name = 'attachments'

detach_dir = plant_functions.attachments_dir(directory_name)

def send_pic():

    row = []
    conn = sqlite3.connect(config.DB_NAME)

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT plant_name, schedule_in_days - days_since_last_water FROM watering_schedule WHERE ignore = 0")

# Hold query in dictionary
    output = {}

# Add items to dictionary
    for row in cursor:
        output[str(row[0])] = row[1]

# Create list of plant names from 'output' dictionary
    plant_list = output.keys()

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

                    if checker == 'request pic':

                        if any(plant in text for plant in plant_list):
                            start = text.find(':')
                            plant = text[start + 2:]

                        pic_path = './pics/' + str(plant) + '.jpg'

                        if os.path.isfile(pic_path):
                        	print 'Sending email with ' + str(plant) + ' pic attached'
                        	plant_functions.send_email('Here is your picture of:',plant,row=None,file_location=pic_path)
                        else:
                        	print 'No plant with that name in pics directory'
                        	plant_functions.send_email('Oh No!', 'There is no plant with that name in your saved pics!')

                        plant_functions.delete_emails(id_list,i,mail)

                    else:
                        print "No add plant emails in inbox"
    else:
        print 'Mailbox is empty!'

send_pic()