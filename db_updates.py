
import sqlite3

# database name to be passed as parameter 
conn = sqlite3.connect('plants.db')

# Create new table with ID as an integer and primary key and Name as a varchar
# This will auto-increment since ID is primary key
conn.execute("create table if not exists watering_schedule (id integer primary key, plant_name varchar(765), schedule_in_days integer, last_watered timestamp, days_since_last_water integer, need_water smallint, ignore smallint)")

conn.execute("create table if not exists score_keeper (id integer primary key, plant_id integer, email varchar(765), timestamp timestamp)")

# Watering Schedule column definitions
# id - table id
# plant_name - name of plant
# schedule_in_days - how often the plant needs to be watered
# last_watered - datetime when plant was last watered
# days_since_last_water - number of days since plant was last watered
# need_water - boolean where 0 means plant does not need water and 1 means plant needs water
# ignore - boolean where 1 means ignore this plant (dead or dormant)

# Score Keeper column definitions
# id - table id
# plant_id - id of plant record from Watering Schedule table
# email - phone number/email address of person who watered table
# timestamp - date the plant was watered

# Note that when we insert, we use the column name we want to insert into and the value. We can skip ID since it will auto-increment

# Insert Examples
# conn.execute("insert into watering_schedule (last_watered) values((SELECT datetime(, 'unixepoch', 'localtime')))")
# conn.execute("insert into watering_schedule (plant_name,schedule_in_days) values('Cacti',30)")

# Delete Examples
# conn.execute("delete from watering_schedule where plant_name = 'rubber_plant' and id = 2")

# Update Examples
# conn.execute("update watering_schedule set days_since_last_water = (SELECT cast(julianday('now') as int)) - (SELECT cast(julianday(last_watered) as int) from watering_schedule where plant_name = 'lemon_tree') where plant_name = 'lemon_tree'")
# conn.execute("update watering_schedule set need_water = 1 where plant_name in ('Lemon Tree', 'Rubber Plant')")
# conn.execute("update watering_schedule set plant_name = 'Jalapeno' where plant_name = 'jalapeno'")
# conn.execute("update watering_schedule set last_watered = '2019-08-10 17:57:39' where plant_name = 'Rubber Plant'")

# Add column example
# conn.execute("alter table watering_schedule add ignore smallint default 0")

# Truncate example
# conn.execute("delete from score_keeper")

# Commit
# conn.commit()

print 'Watering schedule: '
cursor = conn.execute("SELECT * FROM watering_schedule")

for row in cursor:
	print row	

print ''

print 'Score keeper: '
cursor = conn.execute("SELECT * FROM score_keeper")

for row in cursor:
	print row	

conn.close()