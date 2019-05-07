"""
BASICS

Gets all result data and saves it into a JSON file for easiness of future processing
"""


import json
import mysql.connector as mysql_con
import os




boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = "user", password = "password", database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)

# Selects only completed jobs and which have already been received by the server
get_jobs = "SELECT name, cpu_time, create_time, sent_time, received_time FROM result WHERE server_state='5' AND received_time != 0"

cursor.execute(get_jobs)


# All are stored into a dictionary
DATA = {
    "CPU time":[],           # s
    "Created time":[],       # Unix time (s)
    "Job turnaround time":[] # s
}



for (name, cpt, created, sent, received) in cursor:

    # Skip vallidated results
    if str(name[-1]) != "0":
        continue

    DATA["CPU time"].append(cpt)
    DATA["Created time"].append(created)
    DATA["Job turnaround time"].append(received-created)

cursor.close()
boinc_db.close()




with open("boinc_job_data.json", "w") as jf:
    jf.write(json.dumps(DATA, indent=2))
