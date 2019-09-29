
import sqlite3

# database name to be passed as parameter 
conn = sqlite3.connect('plants.db')

# Create new table with ID as an integer and primary key and Name as a varchar
# This will auto-increment since ID is primary key
conn.execute("create table if not exists watering_schedule (id integer primary key, plant_name varchar(765), schedule_in_days integer, last_watered timestamp, days_since_last_water integer, need_water smallint)")
conn.commit()

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

conn.commit()

# cursor = conn.execute("SELECT * FROM watering_schedule")

cursor = conn.execute("SELECT plant_name, schedule_in_days - days_since_last_water FROM watering_schedule")

# for row in cursor:
# 	status = str(row[0]) + ' ' + str(row[1]) + ' days'
# 	print status

output = {}

for row in cursor:
	# print row	
	output[str(row[0])] = row[1]

status = 'Nathona'

print "Water " + status + " in " + str(output.get(status)) + " days"

# print output

conn.close()