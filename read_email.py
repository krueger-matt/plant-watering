# This script runs every hour and checks the Gmail account to see if any plants have been watered.
# If a plant was watered, it updates the db fields:
    # last_watered = now
    # days_since_last_water = 0
    # need_water = 0
# It knows a plant was watered if the user who got the text sends a reply with "Plant Name watered" in that exact syntax.
# If it finds an email saying a plant was watered, it will send a text confirming the action. This is useful
# for situations when multiple people are getting the plant watering texts.
# Make sure the TO = [] line is updated with a phone number for the text to be sent to.

import smtplib
import time
import imaplib
import email as emaily
import os
import sqlite3


FROM_EMAIL  = os.environ.get('FROM_EMAIL')  # Environment variable called FROM_EMAIL set to email address used
FROM_PWD    = os.environ.get('FROM_PWD')    # Environment variable called FROM_PWD set to email password
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# Create a directory for attachments
detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

# Function to go to Gmail and read emails. Checks to find ones with text that = 'Watered'
# If there is a text saying "Plant Name watered" then update datebase column last_watered with current datetime
# After database is updated, send text confirming to all users that the plant has been watered
def read_email_from_gmail():

    row = []
    conn = sqlite3.connect('plants.db')
    cursor = conn.execute("SELECT plant_name FROM watering_schedule where need_water = 1")

    try:
    	# Login to email
    	print "starting"
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        # Loop through all emails starting with earliest ID and incrementing by 1 to highest email ID
        for row in cursor:
            for i in range(first_email_id,latest_email_id + 1, 1):
                typ, data = mail.fetch(i, '(RFC822)' )

                # Grab email data including from, subject, and time
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = emaily.message_from_string(response_part[1])
                        email_subject = msg['subject']
                        if len(email_subject) == 0:
                        	email_subject = '(no subject)'
                        email_from = msg['from']
                        date = msg["Date"]
]
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

                        		# Delete attachments
                        		os.remove(filePath)

                                if text == row[0] + " watered":
                                    conn.execute("update watering_schedule set last_watered = datetime('now'), days_since_last_water = 0, need_water = 0 where plant_name = '" + row[0] + "'")
                                    conn.commit()
                                    print row[0] + ' record updated'

                                    TO = [] # Phone number goes here as a string
                                    SUBJECT = row[0] + ' watered'
                                    email = SUBJECT
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
                                    # Get the mail ID to delete from id_list
                                    id_to_delete = id_list[i-1]
                                    # Delete the email
                                    mail.store("1:{0}".format(id_to_delete), '+X-GM-LABELS', '\\Trash')
                                    print 'Email deleted'



	# Failed login
    except Exception, e:
        print str(e)
        print "failed"

    conn.close()
    print "done"


read_email_from_gmail()