import smtplib
import imaplib
import email as emaily
import os

import config

# Login to email, prepare message, and send mail
# Takes row which is the plant name from the SQL query and email_subect which is defined in whichever script calls this one
def send_email(row,email_subject):

	FROM_EMAIL  = config.FROM_EMAIL
	FROM_PWD    = config.FROM_PWD
	SMTP_SERVER = config.SMTP_SERVER
	SMTP_PORT   = config.SMTP_PORT

	TO = config.TO # Phone number goes here as a string
	SUBJECT = email_subject
	email = SUBJECT
	print SUBJECT

	# Prepare actual message
	message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM_EMAIL, ", ".join(TO), SUBJECT, email)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(FROM_EMAIL, FROM_PWD)
	server.sendmail(FROM_EMAIL, TO, message)
	server.quit()
	print 'Text sent'


# Email login for read_email.py and check_status.py
def email_login():
	FROM_EMAIL  = config.FROM_EMAIL
	FROM_PWD    = config.FROM_PWD
	SMTP_SERVER = config.SMTP_SERVER

	# Login to email
	try:
		print "Logging into email..."
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		mail.login(FROM_EMAIL,FROM_PWD)

		return mail

	# Failed login
	except Exception, e:
		print str(e)
		print "Failed to login!"
		print "Program terminating!"
		quit()


# Parse emails in inbox. Used in read_email.py and check_status.py
def email_parse(detach_dir,response_part):
    msg = emaily.message_from_string(response_part[1])
    email_from = msg['from']
    date = msg["Date"]

    # Download attachments
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
    # Read file
    if bool(fileName):
        filePath = os.path.join(detach_dir, 'attachments', fileName)
        if not os.path.isfile(filePath):
            fp = open(filePath, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            fp = open(filePath, 'r')
            text = fp.read()

            print "Email attachment text: " + str(text)

            # Delete attachments
            os.remove(filePath)

            if text.find(' watered') > 0:
            	checker = text.find(' watered')
            elif text.find(' status') > 0:
            	checker = text.find(' status')
            else:
            	checker = -1

            return checker, text, email_from