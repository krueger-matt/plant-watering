# This script runs anytime after maintenance.py (I have it run at 10am on weekends and 6pm on weekdays) and sends a text for each plant
# that needs to be watered (based on the need_water field in the db).

import sqlite3

import config
import plant_functions

print (plant_functions.current_time())

# Check which plants need water and send a text for each plant if they need water
def send_text():
    print ('Starting...')

    # Add plants to output list if they need water. Send list of all plants in one email with this list
    output = []

    # Checks which plants have a need_water flag set to 1 and then sends one text per plant that needs water
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.execute("SELECT plant_name FROM watering_schedule WHERE need_water = 1 AND ignore = 0")

    # Add items to dictionary
    for row in cursor:
        output.append(row[0])

    if len(output) > 0:
        print (output)
        email_subject = "Plants to water:"
        email_body = ', '.join(output)
        plant_functions.send_email(email_subject,email_body)    
    else:
        print ('No plants need watering')

    conn.close()


send_text()