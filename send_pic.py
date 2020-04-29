# Send a picture of a requested plant to user

import sqlite3
import os

import config
import plant_functions

def send_pic(text):

    row = []
    conn = sqlite3.connect(config.DB_NAME)

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT * FROM watering_schedule")

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

    if any(plant in text for plant in plant_list):
        start = text.find(':')
        plant = text[start + 2:]

    pic_path = './pics/' + str(plant) + '.jpg'

    id                          = str(output.get(plant)[0])
    plant_name                  = str(output.get(plant)[1])
    schedule_in_days            = str(output.get(plant)[2])
    last_watered                = str(output.get(plant)[3])
    days_since_last_water       = str(output.get(plant)[4])
    if output.get(plant)[5] == 0:
    	need_water = 'does not need water'
    elif output.get(plant)[5] == 1:
    	need_water = 'needs to be watered'
    ignore                      = str(output.get(plant)[6])
    has_pic                     = str(output.get(plant)[7])
    latin_name                  = str(output.get(plant)[8])

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

    conn.close()
