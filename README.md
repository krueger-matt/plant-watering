# plant-watering
Python scripts and a SQLite database to help keep track of when to water the plants

Getting started:

Create a new Gmail account and allow less secure apps to access it

Create (or modify the one provided) a SQLite database to keep track of your plants

The database has three tables:

The fields in the watering_schedule table are:
  * id integer primary key,
  * plant_name varchar(765),
  * schedule_in_days integer,
  * last_watered timestamp,
  * days_since_last_water integer,
  * need_water smallint,
  * ignore smallint

The fields in the score_keeper table are:
  * id integer primary key,
  * plant_id integer,
  * email varchar(765),
  * timestamp timestamp

The fields in the emails table are:
  * id integer primary key,
  * email varchar(765),
  * name varchar(765)

Setup a schedule for for maintenance.py to run in the early mornings, send_text.py to run anytime after maintenance.py, read_email.py to run hourly (or more), and check_status.py to run every ten minutes (or more).

Check when your plant needs to be watered next by sending a text with "Plant Name status" as the message

Note that to have Gmail send a message to a phone number, you need to format it differently for different carriers:
  * Verizon: phonenumber@vtext.com
  * AT&T: phonenumber@txt.att.net
  * Sprint: phonenumber@messaging.sprintpcs.com
  * T-Mobile: phonenumber@tmomail.net
