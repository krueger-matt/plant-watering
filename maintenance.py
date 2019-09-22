# This script runs in the early morning. It updates the need_water field if needed and updates the days_since_last_water field on all plants

import smtplib
import time
import imaplib
import email as emaily
import os
import sqlite3

def maintenance():
    conn = sqlite3.connect('plants.db')

    # If days_since_last_water - schedule_in_days is > 0 then we need to update the need_water bool to 1
    cursor = conn.execute("SELECT plant_name, days_since_last_water - schedule_in_days FROM watering_schedule")
    for row in cursor:
        plant = row[0]
        day_diff = row[1]
        print plant, day_diff
        if day_diff >= 0:
                conn.execute("update watering_schedule set need_water = 1 where plant_name = '" + plant + "'")
                conn.commit()
        else:
                conn.execute("update watering_schedule set need_water = 0 where plant_name = '" + plant + "'")
                conn.commit()

        conn.execute("update watering_schedule set days_since_last_water = (SELECT cast(julianday('now') as int)) - (SELECT cast(julianday(last_watered) as int) from watering_schedule where plant_name = '" + plant + "') where plant_name = '" + plant + "'")
    	conn.commit()

    conn.close()


maintenance()