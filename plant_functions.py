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

def current_time():
	return datetime.datetime.now()



# Create a directory for attachments/pics
def attachments_dir(directory_name):
	detach_dir = '.'
	if directory_name not in os.listdir(detach_dir):
	    os.mkdir(directory_name)

	return detach_dir



# Login to email, prepare message, and send mail
# Takes row which is the plant name from the SQL query and email_subect which is defined in whichever script calls this one
def send_email_old(email_subject,email_body,row=None):
	print ('Email Subject: ' + email_subject)
	print ('Email Body: ' + email_body)

	BODY = string.join((
	        "From: %s" % config.FROM_EMAIL,
	        "To: %s" % config.TO,
	        "Subject: %s" % email_subject ,
	        "",
	        email_body
	        ), "\r\n")

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(config.FROM_EMAIL, config.FROM_PWD)
	server.sendmail(config.FROM_EMAIL, config.TO, BODY)
	server.quit()
	print ('Text sent')



def send_email(email_subject,email_body,row=None,file_location=None):
	if len(config.TO) == 1:
		send_to_email = config.TO[0]
	else:
		send_to_email = ','.join(config.TO)

	# file_location = './pics/Jenni Cactus.jpg'

	msg = MIMEMultipart()
	msg['From'] =  config.FROM_EMAIL
	msg['To'] = send_to_email
	msg['Subject'] = email_subject

	msg.attach(MIMEText(email_body, 'plain'))

	# Setup the attachment
	if file_location is not None:
		filename = os.path.basename(file_location)
		attachment = open(file_location, "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

		# Attach the attachment to the MIMEMultipart object
		msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(config.FROM_EMAIL, config.FROM_PWD)
	text = msg.as_string()
	server.sendmail(config.FROM_EMAIL, send_to_email, text)
	server.quit()



# Email login for read_email.py and check_status.py
def email_login():
	try:
		print ("Logging into email...")
		mail = imaplib.IMAP4_SSL(config.SMTP_SERVER)
		mail.login(config.FROM_EMAIL,config.FROM_PWD)

		mail.select('inbox')
		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]

		return mail, mail_ids

	except Exception as e:
		print (str(e))
		print ("Failed to login!")
		print ("Program terminating!")
		quit()



# Parse emails in inbox. Used in read_email.py and check_status.py
def email_parse(detach_dir,response_part,directory_name):
	# msg = email.message_from_string(str(response_part[1]))
	msg = email.message_from_bytes(response_part[1])
	email_from = msg['from']
	date = msg["Date"]
	imagePath = ''
	plant_name = ''
	filePath = ''
	text = ''

	# Download attachments - used for all calls of function
	for part in msg.walk():
		if part.get_content_maintype() == 'multipart':
			continue
		if part.get('Content-Disposition') is None:
			continue
		fileName = part.get_filename()

		if bool(fileName):
			filePath = os.path.join(detach_dir, directory_name, fileName)
			if not os.path.isfile(filePath):
				fp = open(filePath, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
				fp = open(filePath, 'r')
				if filePath.find('.txt') >= 0:
					text = str(fp.read())

			if filePath.find('.jpg') >= 0:
				imagePath = filePath

	# Pic related stuff
	if filePath == './pics/text_1.txt':
		start_text = text.find(':') + 2
		plant_name = text[start_text:].strip()

	if os.path.isfile(imagePath):
		print ('./pics/' + plant_name.strip() + '.jpg')
		os.rename(imagePath,'./pics/' + plant_name + '.jpg')

	print ("Email attachment text: " + str(text))

	# Delete attachments
	os.remove(filePath)

	if text.find(' watered') > 0:
		checker = 'watered'
	elif text.find(' status') > 0:
		checker = 'status'
	elif text.lower().find('get score') >= 0:
		checker = 'get score'
	elif text.lower().startswith('add plant'):
		checker = 'add plant'
	elif text.lower().startswith('add pic'):
		checker = 'add pic'
	elif text.lower().startswith('request pic'):
		checker = 'request pic'
	else:
		checker = -1

	return checker, text, email_from, plant_name



# Total score from score_keeper table by user
def get_overall_score():

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

	return score_list



def delete_emails(id_list,i,mail):
	# Get the mail ID to delete from id_list
	id_to_delete = id_list[i-1]

	print ('Email ID list: ' + ', '.join(id_list))

	print ('Email ID to delete: ' + str(id_to_delete))

	# Delete the email
	mail.store(str(id_to_delete), '+X-GM-LABELS', '\\Trash')
	print ('Email deleted')
