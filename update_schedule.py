# Add a plant via text
# To use, text "Add Plant: plant_name, schedule in days" in that exact syntax. It will automatically create a row in the
# watering_schedule table, populate the current time as last_watered, and 0 for all of the other fields

import sqlite3

import config
import plant_functions

def update_schedule(text):

    if text.lower().startswith('update schedule'):
        conn = sqlite3.connect(config.DB_NAME)
        start_text = text.find(':') + 2
        end_text = text.find(',')
        plant_name = text[start_text:end_text]

        schedule_in_days = text[end_text + 2:]

        sql = "UPDATE watering_schedule SET schedule_in_days = " + str(schedule_in_days) + " WHERE plant_name = '" + str(plant_name) + "'"

        print (sql)

        cursor = conn.execute(sql)
        conn.commit()

        email_subject = 'Schedule updated:'
        email_body = "Updated " + plant_name + " to watering schedule of " + str(schedule_in_days)

        plant_functions.send_email(email_subject,email_body)

        conn.close()
