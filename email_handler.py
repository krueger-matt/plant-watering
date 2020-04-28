import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sqlite3
import string
import datetime

import config
import plant_functions
import check_status
import get_score
import add_plant
import plant_watered

def email_login_new():

	print (plant_functions.current_time())
	
	try:
		print ("Logging into email...")
		mail = imaplib.IMAP4_SSL(config.SMTP_SERVER)
		mail.login(config.FROM_EMAIL,config.FROM_PWD)

		mail.select('inbox')
		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		# return mail, mail_ids

		directory_name = 'attachments'
		detach_dir = plant_functions.attachments_dir(directory_name)

		if len(mail_ids) > 0:
			id_list = mail_ids.decode().split()
			first_email_id = int(id_list[0])
			latest_email_id = int(id_list[-1])

			for i in range(first_email_id,latest_email_id + 1, 1):
				print ("i: " + str(i))

				typ, data = mail.fetch(str(i), '(RFC822)' )

				for response_part in data:
					if isinstance(response_part, tuple):
						email_parse_results = plant_functions.email_parse(detach_dir,response_part,directory_name)
						checker = email_parse_results[0]
						text = email_parse_results[1]
						email_from = email_parse_results[2]

						print ("checker: " + str(checker))

						if checker == 'watered':
							plant_watered.plant_watered(text,email_from)
							plant_functions.delete_emails(id_list,i,mail)							
						elif checker == 'status':
							check_status.check_status(text)
							plant_functions.delete_emails(id_list,i,mail)
						elif checker == 'get score':
							get_score.get_score(text)
							plant_functions.delete_emails(id_list,i,mail)
						elif checker == 'add plant':
							add_plant.add_plant(text)
							plant_functions.delete_emails(id_list,i,mail)
						else:
							print ("No emails in inbox match the patterns accepted.")

		else:
			print ('Mailbox is empty!')


	except Exception as e:
		print (str(e))
		print ("Failed to login!")
		print ("Program terminating!")
		quit()


email_login_new()