"""
BASICS

Reads the files and saves the result times to a json file for future processing
"""


import datetime
import json
import os


dirnames = ["vina", "bedtools", "blast", "bowtie", "gromacs", "htseq", "lammps", "namd", "opsees"]
appnames = ["AutoDock Vina", "Bedtools", "Blast", "Bowtie", "Gromacs", "HTSeq", "MPI-LAMMPS", "NAMD", "OpenSees"]




# Finds the time needed to process a stampede job given a file
def runtime(filename):

    with open(filename, "r") as ff:
        for line in ff:
            LL = timestamp = line.split(" ")

            if "Start" == LL[0]:
                start_time = datetime.datetime.strptime(LL[6], "%H:%M:%S")

            if "End" == LL[0]:
                end_time = datetime.datetime.strptime(LL[6], "%H:%M:%S")
                return (end_time-start_time).seconds



# Finds the overall time needed for a job using a tracker file
def complete_time_to_process(filename):

    with open(filename, "r") as ff:
        for line in ff:
            LL = timestamp = line.split(" ")

            if "Tracker:" == LL[0]:
                tracker_number = LL[1].replace("\n", "")

            if "End" == LL[0]:
                end_time = datetime.datetime.strptime(LL[6], "%H:%M:%S")
                break

    # Assumed that the tracker file is in the same directory as the main file
    dirboth = filename.split("/")
    dirboth = "/".join(dirboth[:len(dirboth)-1:])
    with open(dirboth+"/tracker_"+tracker_number+".txt", "r") as ff:
        for line in ff:
            LL = timestamp = line.split(" ")

            if "Start" == LL[0]:
                start_time = datetime.datetime.strptime(LL[6], "%H:%M:%S")
                return (end_time-start_time).seconds




stampede2_times = {}

for dirname, appname in zip(dirnames, appnames):

    # Finds the files needed
    slurm_result_files = [dirname+"-test/"+file for file in os.listdir(dirname+"-test") if file.startswith("slurm") and file.endswith(".out") ]
    stampede2_times[appname] = {}
    stampede2_times[appname]["runtime"] = [runtime(slurm_file) for slurm_file in slurm_result_files]

    stampede2_times[appname]["complete_time"] = [complete_time_to_process(slurm_file) for slurm_file in slurm_result_files]


# Saves result to a json file
with open("stampede2_results.json", "w") as ff:
    ff.write(json.dumps(stampede2_times, indent=4))



