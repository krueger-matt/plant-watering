# Checks if eligible plants have been watered and updates the score_keeper table when plants are watered

import sqlite3

import config
import plant_functions

def plant_watered(text,email_from):

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.execute("SELECT plant_name FROM watering_schedule WHERE need_water = 1 AND ignore = 0")

    # Loop through all of the plant_names that the SQL query above pulled (all plants where need_water = 1)
    for row in cursor:

        print ('Looking for ' + str(row[0]))

        if text.strip() == row[0] + " watered":
            conn.execute("UPDATE watering_schedule SET last_watered = datetime('now'), days_since_last_water = 0, need_water = 0 WHERE plant_name = '" + row[0] + "'")
            conn.commit()

            plant_name = row[0]

            print (plant_name + ' record updated')

            # New cursor to run query to get plant_id
            plant_id_cursor = conn.execute("SELECT id FROM watering_schedule WHERE plant_name = '" + plant_name + "'")

            # Get actual plant_id from the cursor
            for plant in plant_id_cursor:
                plant_id = plant[0]

            score_keeper_sql = ("INSERT INTO score_keeper (plant_id,email,timestamp) VALUES (" + str(plant_id) + ",'" + email_from + "',date('now'))")
            print (score_keeper_sql)

            # Insert plant_id and email into score_keeper table
            conn.execute(score_keeper_sql)
            conn.commit()

            email_subject = 'Updates:'
            email_body = row[0] + ' watered'
            plant_functions.send_email(email_subject,email_body,row)

    conn.close()
