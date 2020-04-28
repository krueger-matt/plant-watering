# This checks if anyone has texted Get Score and responds with the current score from the score_keeper table

import sqlite3

import config
import plant_functions

def get_score(text):

    if text.strip().lower() == "get score":

        # Create email subject to pass to plant_functions
        email_body = plant_functions.get_overall_score()
        email_body = str(email_body)
        email_subject = "Overall score:"

        # Call plant_functions and pass row and email subject
        plant_functions.send_email(email_subject,email_body)
