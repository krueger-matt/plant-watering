# This checks if anyone has texted Get Score and responds with the current score from the score_keeper table

import config
import plant_functions

def help(text):

	if text.strip().lower() == "help":

		email_body = '''
Add a picture of a plant by texting "Add Pic: plant_name"\n
Add a plant by texting "Add Plant: plant_name, schedule_in_days"\n
Check status of one plant by texting "plant_name status"\n
Check status of all plants by texting "All status" \n
Confirm a plant has been watered by texting "plant_name watered"\n
Get a picture of a plant texted to you by texting "Request Pic: plant_name"\n
Get list of plants that need to be watered in the next 7 days by texting "7 day status"\n
Get score of users (how many plants each user has watered) by texting "Get Score"\n
Update a plant's watering schedule by texting "Update Schedule: plant_name, schedule_in_days"'''

		email_subject = "Available Commands:"

		plant_functions.send_email(email_subject,email_body)