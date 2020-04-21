# plant-watering
Python scripts and a SQLite database to help keep track of when to water the plants

Getting started:

Create a new Gmail account and allow less secure apps to access it

Create (or modify the one provided) a SQLite database to keep track of your plants

The database has three tables:
  * watering_schedule   - A list of all the plants, their watering schedule, and if they need water
  * score_keeper        - A list of all the times someone has texted that they have watered a plant
  * emails              - A list of users

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

#### Usage and Features:
  * Add a picture of a plant by texting "Add Pic: plant_name"
    * Example: Add Pic: Palm Tree
  * Add a plant by texting "Add Plant: plant_name, schedule_in_days"
    * Example: Add Plant: Palm Tree, 17
  * Check status of one plant by texting "plant_name status"
    * Example: Lemon Tree status
  * Check status of all plants by texting "All status"
  * Confirm a plant has been watered by texting "plant_name watered"
    * Example: Lemon Tree watered
    * Note: You can only water a plant that has indicated it needs to be watered
  * Get a picture of a plant texted to you by texting "Request Pic: plant_name"
    * Example: Request Pic: Palm Tree
  * Get list of plants that need to be watered in the next 7 days by texting "7 day status"
  * Get score of users (how many plants each user has watered) by texting "Get Score"

