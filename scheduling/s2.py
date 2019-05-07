#!/usr/bin/python3

"""
BASICS

Analyzes the BOINC data to find the function parameters
"""


import datetime
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as LA
import pickle
import random
import scipy.stats as stats


import statistical_functions as sf



# TACC SLURM stores dates in local time
def dt_from_unix_timestamp(unix_timestamp):
    return datetime.datetime.fromtimestamp(unix_timestamp)






##################
# Preprocessing
##################


submit_date = [] # Job was submitted on this date
complete_time = [] # Time for completion
N_nodes = [] # Number of nodes
n_CPUs = []  # Number of allocated CPUs
guessed_runtime = []



cou = 0

# Reads the data
with open("s2_data/completed_stampede2_slurm.txt", "r") as ff:

    for line in ff:

        if cou == 0:
            cou += 1
            continue

        LL = line.split("|")

        # Everything above 4 nodes requested is not to be run on BOINC, exempt from analysis
        if int(LL[4]) > 4:
            continue

        runtime = float(LL[1]) - float(LL[2])

        # Skips jobs run in less than 5 s, probably tests
        if runtime < 5:
            continue

        # Assumes that the user knows the correct runtime by between 50% and 100%, 
        guessed_runtime.append(runtime*random.uniform(0.8, 1.2))


        submit_date.append(dt_from_unix_timestamp(float(LL[3])))
        complete_time.append(int(LL[1]) - int(LL[2])  )
        N_nodes.append(int(LL[4]))
        n_CPUs.append(int(LL[5]))

        # Restrict to the first 600000 rows so that it is not too much
        if cou > 600000:
            break

        cou += 1


S2_data = {
    "Submission date":submit_date,
    "Job turnaround time":complete_time,
    "N Nodes":N_nodes,
    "n CPUs":n_CPUs,
    "guessed runtime":guessed_runtime
}


# Writes to pickle file for easier future processing
with open("s2_data/preprocessed.pckl", "wb") as pf:
    pickle.dump(S2_data, pf)


# Loads the S2 data
with open("s2_data/preprocessed.pckl", "rb") as datafile:
    S2_data = pickle.load(datafile)





##########################
# Functions to compute
# All have an input j, equal to the position in the S2 Slurm data dictionary array to search
# 
##########################


# 1 for wokdays, 0 for not: workdays are Monday, Tuesday, Wednesday, Thursday, Friday
def workday_or_not(j):
    wday = S2_data["Submission date"][j].weekday()

    if wday < 5:
        return True
    else:
        return False



# 1 for workhours, 0 for not: workhours are defined as those between 13:00 and 23:00 UTC
# these correspond to 8:00-18:00 during summer daylight time
def workhours_or_not(j):
    whours = S2_data["Submission date"][j].hour

    if (whours > 8) and (whours < 18):
        return True
    else:
        return False



# Computes how useful these  hours are using sine function
def cardiac_whours(j):

    whours = S2_data["Submission date"][j].hour 
    val1 = math.sin((whours-8)*math.pi/10)
    return np.sign(val1)*abs(val1)**0.5



# 1 for day, 0 for night
# Day defined between 06:00 and 20:00
def day_or_night(j):
    whours = S2_data["Submission date"][j].hour

    if (whours > 5) and (whours < 20):
        return True
    else:
        return False



# Returns the number of nodes 
def node_count(j):
    return S2_data["N Nodes"][j]


# Returns the number of nodes 
def cpu_count(j):
    return S2_data["n CPUs"][j]


def user_provided_runtime(j):
    return S2_data["guessed runtime"][j]


def constant_C(j):
    return 1



##########################
# Linear Least-Squares
# 
##########################


number_of_completed_jobs = len(S2_data["Job turnaround time"])



used_functions = [
                workday_or_not,
                workhours_or_not,
                cardiac_whours,
                day_or_night,
                node_count,
                cpu_count,
                user_provided_runtime,
                constant_C
                ]


Betas = sf.gauss_solve(used_functions, S2_data["Job turnaround time"])
ls_obtained_QoS_times = sf.fitted_result(Betas, used_functions, list(hjk for hjk in range(0, number_of_completed_jobs)))


# Prints the coefficients together with the functions name
for hh in range(0, len(Betas)):
    print(str(Betas[hh])+" * "+used_functions[hh].__name__)



print("Least-Squares Results:")
print("R**2 =", sf.R2(S2_data["Job turnaround time"], ls_obtained_QoS_times))
print("RMS error =", sf.RMS_error(S2_data["Job turnaround time"], ls_obtained_QoS_times))
print("RMS relative error =", sf.RMS_rel_error(S2_data["Job turnaround time"], ls_obtained_QoS_times))



# Computes the errors
ecalcs = np.array(S2_data["Job turnaround time"]) - np.array(ls_obtained_QoS_times)




stats.probplot(ecalcs, dist="norm", plot=plt)
plt.title("Residuals: Q-Q")





plt.figure()
plt.plot(ecalcs, 'ko')
plt.title("Residuals")
plt.xlabel("Job number")
plt.ylabel("Residual")



plt.show()
















