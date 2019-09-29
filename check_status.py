# This script runs every 10 minutes. It checks if anyone has emailed a plant name which means they want to know when it should be watered next
# If it finds an email with a plant name, it sends a text back saying when the plant next needs water
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

# Function to go to Gmail and read emails
# Looks for emails with just a plant name in them
# Sends a text to users with the number of days until that plant needs to be watered
def check_status():

    row = []
    conn = sqlite3.connect('plants.db')

# Query to get plant names and days until next water
    cursor = conn.execute("SELECT plant_name, schedule_in_days - days_since_last_water FROM watering_schedule")

# Hold query in dictionary
    output = {}

# Add items to dictionary
    for row in cursor:
        output[str(row[0])] = row[1]

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

                            # text is the name of the plant that the user asked for
                            # status is the number of days until that plant needs to be watered (stored in the output dictionary)
                            status = output.get(text)
                            # status_text is the actual message that will get sent back, telling all users when that plant needs to be watered
                            status_text =  "Water " + text + " in " + str(status) + " days"

                            TO = [] # Phone number goes here as a string
                            SUBJECT = status_text
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


check_status()