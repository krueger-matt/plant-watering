# Update db 'has_pic' column to 1 when a picture is added to the pics folder

import sqlite3

import config

def add_pic(plant_name):

    conn = sqlite3.connect(config.DB_NAME)
    conn.execute("UPDATE watering_schedule SET has_pic = 1 WHERE plant_name = '" + plant_name + "'")
    conn.commit()
    conn.close()

    print ('DB has_pic column has been set to 1 for ' + plant_name)
