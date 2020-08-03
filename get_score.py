# This checks if anyone has texted Get Score and responds with the current score as well as the last 30 day score 
# from the score_keeper table 

import sqlite3

import config
import plant_functions

def get_score(text):

	if text.strip().lower() == "get score":

		score_list = []
		score_last_30_days = []

		sql_score_list = """SELECT e.name, count(sk.id) 
								 FROM score_keeper sk 
								 JOIN emails e ON sk.email = e.email 
								 GROUP BY 1 ORDER BY 2 DESC"""

		sql_last_30_list = """SELECT e.name, count(sk.id) 
								 FROM score_keeper sk
								 JOIN emails e ON sk.email = e.email
								 WHERE timestamp >= date('now','-30 days')
								 GROUP BY 1 ORDER BY 2 DESC"""

		sqls = [sql_score_list, sql_last_30_list]
		lists = [score_list, score_last_30_days]

		conn = sqlite3.connect(config.DB_NAME)

		x = 0

		for sql in sqls:
			cursor = conn.execute(sql)

			if x == 0:
				print ('Overall score:')
			elif x ==1:
				print ('Last 30 days:')

			for row in cursor:
				print (str(row[0]) + ": " + str(row[1]))
				lists[x].append(str(row[0]) + ": " + str(row[1]))

			x+=1

		email_body = 'Overall Score:\n' + str(score_list) + '\n' + 'Last 30 Days:\n' + str(score_last_30_days)

		email_subject = "Plant Bot Scores:"

		plant_functions.send_email(email_subject,email_body)

		conn.close()
