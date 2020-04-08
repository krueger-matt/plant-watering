import smtplib

import config

# Login to email, prepare message, and send mail
# Takes row which is the plant name from the SQL query and email_subect which is defined in whichever script calls this one
def email_login(row,email_subject):

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