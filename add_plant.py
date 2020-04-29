# Add a plant via text
# To use, text "Add Plant: plant_name, schedule in days" in that exact syntax. It will automatically create a row in the
# watering_schedule table, populate the current time as last_watered, and 0 for all of the other fields

import sqlite3

import config
import plant_functions

def add_plant(text):

    if text.startswith('Add Plant:'):
        conn = sqlite3.connect(config.DB_NAME)
        start_text = text.find(':') + 2
        end_text = text.find(',')
        plant_name = text[start_text:end_text]

        schedule_in_days = text[end_text + 2:]

        sql = "INSERT INTO watering_schedule (plant_name, schedule_in_days, last_watered, days_since_last_water, need_water, ignore) VALUES ('" + str(plant_name + "','" + str(schedule_in_days) + "', (SELECT datetime('now','localtime')), 0, 0, 0)")

        print (sql)

        cursor = conn.execute(sql)
        conn.commit()

        email_subject = 'Plant Added:'
        email_body = "Added " + plant_name + " with watering schedule of " + str(schedule_in_days) + " days to plants database!"

        plant_functions.send_email(email_subject,email_body)

        conn.close()
