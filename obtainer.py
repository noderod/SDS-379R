"""
BASICS

Obtains the results and writes them into an easier to a JSON file, easier to process in the future
"""

import datetime
import json
import mysql.connector as mysql_con
import os, shutil


results_dir = "/results/boinc2docker/"
analysis_dir = "/home/boincadm/project/sds3793/"



# Provided two dates in Unix timestamp form, it returns the data in an array form
# Returns [filenames, datetimes]
# date1, date2 (int): Unix timestamps
def obtain_information(date1, date2):

    boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = "user", password = "password", database = 'boincserver')
    cursor = boinc_db.cursor(buffered=True)

    # Selects those between the timestamps and ignores those that have not been received, selects only those jobs that have been completed by the volunteers
    find_files = "SELECT name, cpu_time, create_time, sent_time, received_time FROM result WHERE (create_time BETWEEN %s AND  %s) AND received_time != 0"

    cursor.execute(find_files, (date1, date2))

    completed_names, cpu_times, created_times, sent_times, received_times = [[], [], [], [], []]

    for (name, cpt, created, sent, received) in cursor:

        # Skip vallidated results
        if str(name[-1]) != "0":
            continue

        completed_names.append(name)
        cpu_times.append(cpt)
        created_times.append(created)
        sent_times.append(sent)
        received_times.append(received)

    cursor.close()
    boinc_db.close()

    return [completed_names, cpu_times, created_times, sent_times, received_times]



# Obtains the day given a certain Unix timestamp
# Date is in format YYYY-MM-DD (str)
# unix_timestamp (int)
def YYYYMMDD_from_unix_timestamp(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')



# Given an application name, and a list of lists containing two datetimes each, it creates a directory, and moves the files there
# appname (str)
def result_file_mover(appname, arrdates):

    appdir = analysis_dir+appname+"/"

    if not os.path.isdir(appdir):
        os.mkdir(appdir)

    INFO = [[], [], [], [], []]

    for dates in arrdates:
        new_info = obtain_information(dates[0], dates[1])

        for loc, nloc in zip(INFO, new_info):
            loc += nloc


    # Extra row to see if the job returned files
    INFO.append([])

    for fnam, timestamp in zip(INFO[0], INFO[4]):

        path_location = results_dir+YYYYMMDD_from_unix_timestamp(timestamp)+"/"

        # Finds the file
        filename = [file for file in os.listdir(path_location) if file.startswith(fnam)]

        if filename == []:
            INFO[-1].append(0)
            continue
        else:
            filename = filename[0]
            INFO[-1].append(1)

        # Copies it to destination
        shutil.copyfile(path_location+filename, appdir+fnam)

    # Writes a json file with the data
    with open(appdir+"summary.json", "w") as ff:
        ff.write(json.dumps({"cpu_times":INFO[1], "overall_time":list(float(x) for x in np.array(INFO[4]) - np.array(INFO[2])), "successful":INFO[-1]}, indent=2))



"""
app,start time,end time
autodock-vina,1556479349,1556479460
autodock-vina,1556492271,1556492395
OpenSees,1556479621,1556479746
Blast,1556479791,1556479869
Bedtools,1556479900,1556479980
MPI-Lammps,1556480025,1556480089
Gromacs,1556483049,1556483116
HTSeq,1556483149,1556483210
NAMD,1556483239,1556483290
Bowtie,1556483311,1556483370
"""



appall = {
    "AutoDock-Vina":[[1556821560,1556827159]],
    "OpenSees":[[1556744680,1556747676]],
    "Blast":[[1556832947,1556835815]],
    "Bedtools":[[1556835869,1556838478]],
    "MPI-Lammps":[[1556671520,1556673871]],
    "Gromacs":[[1556838527,1556841297]],
    "HTSeq":[[1556841319,1556843497]],
    "NAMD":[[1556843532,1556845684]],
    "Bowtie":[[1556845698,1556847930]]
}


for app_to_run in appall:
    result_file_mover(app_to_run, appall[app_to_run])

