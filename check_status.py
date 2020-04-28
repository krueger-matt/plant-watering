# Check when a plant or when all plants need to be watered next

import sqlite3
import operator

import config
import plant_functions


def check_status(text):

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

    conn.close()
