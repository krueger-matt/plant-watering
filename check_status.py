# Check when a plant or when all plants need to be watered next

import sqlite3
import operator

import config
import plant_functions

print (plant_functions.current_time())

directory_name = 'attachments'

detach_dir = plant_functions.attachments_dir(directory_name)

# Function to go to Gmail and read emails
# Looks for emails with just a plant name in them
# Sends a text to users with the number of days until that plant needs to be watered
def check_status():

    row = []
    conn = sqlite3.connect(config.DB_NAME)

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT plant_name, schedule_in_days - days_since_last_water FROM watering_schedule WHERE ignore = 0")

# Hold query in dictionary
    output = {}

# Add items to dictionary
    for row in cursor:
        output[str(row[0])] = row[1]

    sorted_output = sorted(output.items(), key=operator.itemgetter(1))

# Create list of plant names from 'output' dictionary
    plant_list = output.keys()

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

                    if checker == 'status':

                        print ("checker: " + str(checker))

                        # Check the status of one plant
                        if any(plant in text for plant in plant_list):

                            # removed_string takes the text variable, which is the email attachment, and removes the ' status' portion in order to get the plant name
                            removed_string = text.find(' status')
                            plant = text[0:removed_string]

                            # status is the number of days until that plant needs to be watered (stored in the output dictionary)
                            status = output.get(plant)

                            # Create email subject to pass to plant_functions
                            email_subject = 'Status:'
                            email_body = "Water " + plant + " in " + str(status) + " days"

                        # Return all plants status
                        elif text.strip().lower() == "all status":
                            email_subject = 'Overall Status:'
                            email_body = 'Water:\n'
                            for plant in sorted_output:
                                email_body = email_body + str(plant[0]) + ' in ' + str(plant[1]) + ' days\n'

                        # Return plants that need to be watering in the next 7 days
                        elif text.strip().lower() == "7 day status":
                            seven_day_dict = {}
                            for k,v in output.items():
                                if v <= 7:
                                    seven_day_dict[k] = v

                            sorted_seven_day_dict = sorted(seven_day_dict.items(), key=operator.itemgetter(1))

                            email_subject = 'Next 7 Days:'
                            email_body = 'Water:\n'
                            for plant in sorted_seven_day_dict:
                                email_body = email_body + str(plant[0]) + ' in ' + str(plant[1]) + ' days\n'
                        
                        plant_functions.send_email(email_subject,email_body,row)

                        plant_functions.delete_emails(id_list,i,mail)

                    else:
                        print ("No status emails in inbox")

        conn.close()
        print ("Done")

    else:
        print ('Mailbox is empty!')


check_status()