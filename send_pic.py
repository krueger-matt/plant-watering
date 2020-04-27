# Send a picture of a requested plant to user

import sqlite3
import os

import config
import plant_functions

print (plant_functions.current_time())

directory_name = 'attachments'

detach_dir = plant_functions.attachments_dir(directory_name)

def send_pic():

    row = []
    conn = sqlite3.connect(config.DB_NAME)

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT * FROM watering_schedulE")

    plant_list = []

    output = {}

# Add items to list
    for row in cursor:
        plant_list.append(row[1]) # plant_name
        plant_list.append(str(row[8])) # latin_name
        lst = []
        for data_point in row:
        	lst.append(data_point)
        # print (lst)
        output[str(row[1])] = lst

    # print (output)
    # Dictionary keys are plant names. Values are all records from DB
    # This pulls the recordf or Lemon Tree from the dictionary and then just pulls the 8th indexed spot in the list of values (latin_name)
    # print (output.get('Lemon Tree')[8])

    # sys.exit()

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

                    if checker == 'request pic':

                        if any(plant in text for plant in plant_list):
                            start = text.find(':')
                            plant = text[start + 2:]

                        pic_path = './pics/' + str(plant) + '.jpg'

                        id = str(output.get(plant)[0])
                        plant_name = str(output.get(plant)[1])
                        schedule_in_days = str(output.get(plant)[2])
                        last_watered = str(output.get(plant)[3])
                        days_since_last_water = str(output.get(plant)[4])
                        if output.get(plant)[5] == 0:
                        	need_water = 'does not need water'
                        elif output.get(plant)[5] == 1:
                        	need_water = 'needs to be watered'
                        ignore = str(output.get(plant)[6])
                        has_pic = str(output.get(plant)[7])
                        latin_name = str(output.get(plant)[8])

                        if os.path.isfile(pic_path):
                        	email_body = (f"""{plant_name} (Latin name: {latin_name}).
It should be watered every {schedule_in_days} days. 
It has been {days_since_last_water} days since it was last watered.
Its current {need_water}.
Here is a picture:""")
                        	print ('Sending email with ' + str(plant) + ' pic attached')
                        	plant_functions.send_email('You inquired about:',email_body,row=None,file_location=pic_path)
                        else:
                        	print ('No plant with that name in pics directory')
                        	plant_functions.send_email('Oh No!', 'There is no plant named ' + plant + ' in your saved pics!')

                        plant_functions.delete_emails(id_list,i,mail)

                    else:
                        print ("No add plant emails in inbox")
    else:
        print ('Mailbox is empty!')

send_pic()