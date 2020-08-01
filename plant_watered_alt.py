# Takes single integer as plant ID from a text and updates need_water status/sends email

import sqlite3

import config
import plant_functions

def plant_watered(text,email_from):

    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.execute("SELECT id FROM watering_schedule WHERE need_water = 1 AND ignore = 0")

    id_list = []

    for row in cursor:
        id_list.append(row[0])

    print("List of IDs that need water")
    print (id_list)

    if int(text) in id_list:

        print(text + ' to be processed')

        sql = "UPDATE watering_schedule SET last_watered = datetime('now'), days_since_last_water = 0, need_water = 0 WHERE id = " + text
        print (sql)
        conn.execute(sql)
        conn.commit()

        print (text + ' record updated')

        score_keeper_sql = ("INSERT INTO score_keeper (plant_id,email,timestamp) VALUES (" + text + ",'" + email_from + "',date('now'))")
        print (score_keeper_sql)
        conn.execute(score_keeper_sql)
        conn.commit()

        email_subject = 'Updates:'
        email_body = text + ' watered'
        plant_functions.send_email(email_subject,email_body,row)

    conn.close()
