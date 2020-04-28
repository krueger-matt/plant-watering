# This checks if anyone has texted Get Score and responds with the current score from the score_keeper table

import sqlite3

import config
import plant_functions

def get_score(text):

	if text.strip().lower() == "get score":

		score_list = []

		conn = sqlite3.connect(config.DB_NAME)
		cursor = conn.execute("""SELECT e.name, count(sk.id) 
								 FROM score_keeper sk 
								 JOIN emails e ON sk.email = e.email 
								 GROUP BY 1 ORDER BY 2 DESC""")

		print ('Overall score:')

		for row in cursor:
			print (str(row[0]) + ": " + str(row[1]))
			score_list.append(str(row[0]) + ": " + str(row[1]))

		email_body = str(score_list)
		email_subject = "Overall score:"

		plant_functions.send_email(email_subject,email_body)

		conn.close()
