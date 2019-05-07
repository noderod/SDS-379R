"""
BASICS

Obtains user, host information from the BOINC database and stores it into a text file
Volunteer information recorded: number ID, joined time
Host information recorded: number ID, joined  time, CPU, OS
"""

import json
import mysql.connector as mysql_con
import os




boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = "user", password = "password", database = 'boincserver')
cursor1 = boinc_db.cursor()
cursor2 = boinc_db.cursor()


# Gets the volunteer data
volunteer_data = "SELECT id, create_time FROM user"
cursor1.execute(volunteer_data)

user_ids = []
created_times = []


for (user_id, create_time) in cursor1:
    user_ids.append(user_id)
    created_times.append(create_time)



# Gets the host data
host_data = "SELECT userid, create_time, os_name FROM host"
cursor2.execute(host_data)

host_userid = []
os_names = []
time_joined = []
for (userid, tj, os_name) in cursor2:
    host_userid.append(userid)
    time_joined.append(tj)
    os_names.append(os_name)

cursor1.close()
cursor2.close()
boinc_db.close()



DATA = {
    
    "users":{
            "id":user_ids,
            "join time":created_times
    },

    "hosts":{
            "user id":host_userid,
            "join time": time_joined,
            "os":os_names
    }

}

with open("users_hosts.json", "w") as ff:
    ff.write(json.dumps(DATA, indent=2))
