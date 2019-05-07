#!/usr/bin/python3

"""
BASICS

Analyzes the BOINC data to find the function parameters
"""


import datetime
import json
from keras.models import Sequential
from keras.layers import Dense, Dropout
import math
import numpy as np
import numpy.linalg as LA
import pickle
import random


import statistical_functions as sf




# Obtains the date from Unix time
def dt_from_unix_timestamp(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp)



# Print a date in format YYYY-MM-DD
def timformat(dt):
    return dt.strftime("%Y-%m-%d")



##########################
# Loads the necessary data
##########################

# Loads the host data
with open("../hosts_per_day.json", "r") as datafile:
    Host_data = json.load(datafile)


"""
# Preprocessing has been completed, now reading from a file



# Loads the BOINC data
with open("boinc_data/boinc_job_data.json", "r") as datafile:
    BOINC_raw_data = json.load(datafile)




# Changes certain times to make it easier to process later
# Ignores jobs which CPU time is 0, this indicates a fault in the client part
BOINC_data = {
            "CPU time":[],
            "Created time":[],
            "Job turnaround time":[],

            "1H submitted": [], # Jobs submitted in the past 1 H
            "1H completed": [], # Jobs submitted in the past 1 H completed so far
            "1H completed time avg":[], # Avg complete time for jobs submitted in the last 1 H

            "4H submitted": [], # Jobs submitted in the past 4 H
            "4H completed": [], # Jobs submitted in the past 4 H completed so far
            "4H completed time avg":[], # Avg complete time for jobs submitted in the last 4 H

            "1W submitted": [], # Jobs submitted in the past week
            "1W completed": [], # Jobs submitted in the past week completed so far
            "1W completed time avg":[] # Avg complete time for jobs submitted in the last week
            }


t_delta__1h = datetime.timedelta(hours=1)
t_delta__4h = datetime.timedelta(hours=4)
t_delta__1w = datetime.timedelta(days=7)


print("Preprocessing: ")
for qq in range(0, len(BOINC_raw_data["CPU time"])):

    if BOINC_raw_data["CPU time"][qq] == 0:
        continue

    BOINC_data["CPU time"].append(BOINC_raw_data["CPU time"][qq])
    BOINC_data["Created time"].append(dt_from_unix_timestamp(BOINC_raw_data["Created time"][qq]))
    BOINC_data["Job turnaround time"].append(BOINC_raw_data["Job turnaround time"][qq])


    # Computes the average turnaround time to complete a job
    current_date = BOINC_data["Created time"][-1]
    current_pos = len(BOINC_data["Created time"])-1

    # 4 h check


    # If there are more than 5000 jobs preceding this one, uses the 5000 preceding it
    if (current_pos+1) < 5001:
        jobs_to_be_checked = BOINC_data["Created time"]
    else:
        jobs_to_be_checked = BOINC_data["Created time"][current_pos-5000::]


    jobs_submitted_less_than_4h = [z for z in range(0, len(jobs_to_be_checked)) if jobs_to_be_checked[z] > (current_date - t_delta__4h)]
    jobs_submitted_so_far = (len(BOINC_data["Created time"])-1) # Does not include itself


    # Jobs completed within those submitted less than 4 H ago
    completed_4h_ago = [w for w in jobs_submitted_less_than_4h if BOINC_data["Job turnaround time"][w] < 14400]

    BOINC_data["4H submitted"].append(len(jobs_submitted_less_than_4h))


    # If no jobs have been completed in the past 4 H
    if completed_4h_ago == []:
        BOINC_data["4H completed"].append(0)
        BOINC_data["4H completed time avg"].append(0)
    else:
        BOINC_data["4H completed"].append(len(completed_4h_ago)/len(jobs_submitted_less_than_4h))
        BOINC_data["4H completed time avg"].append(np.mean([BOINC_data["Job turnaround time"][zi] for zi in completed_4h_ago]))







    # 1 h
    # If there are more than 1000 jobs preceding this one, uses the 5000 preceding it
    if (current_pos+1) < 1001:
        jobs_to_be_checked = BOINC_data["Created time"]
    else:
        jobs_to_be_checked = BOINC_data["Created time"][current_pos-1000::]


    jobs_submitted_less_than_1w = [z for z in range(0, len(jobs_to_be_checked)) if jobs_to_be_checked[z] > (current_date - t_delta__1h)]
    jobs_submitted_so_far = (len(BOINC_data["Created time"])-1) # Does not include itself


    # Jobs completed within those submitted less than 1 H ago
    completed_1w_ago = [w for w in jobs_submitted_less_than_1w if BOINC_data["Job turnaround time"][w] < 3600]

    BOINC_data["1H submitted"].append(len(jobs_submitted_less_than_1w))


    # If no jobs have been completed in the past 1 H
    if completed_1w_ago == []:
        BOINC_data["1H completed"].append(0)
        BOINC_data["1H completed time avg"].append(0)
    else:
        BOINC_data["1H completed"].append(len(completed_1w_ago)/len(jobs_submitted_less_than_1w))
        BOINC_data["1H completed time avg"].append(np.mean([BOINC_data["Job turnaround time"][zi] for zi in completed_1w_ago]))








    # 1 week
    # If there are more than 15000 jobs preceding this one, uses the 5000 preceding it
    if (current_pos+1) < 15001:
        jobs_to_be_checked = BOINC_data["Created time"]
    else:
        jobs_to_be_checked = BOINC_data["Created time"][current_pos-15000::]


    jobs_submitted_less_than_1w = [z for z in range(0, len(jobs_to_be_checked)) if jobs_to_be_checked[z] > (current_date - t_delta__1h)]
    jobs_submitted_so_far = (len(BOINC_data["Created time"])-1) # Does not include itself


    # Jobs completed within those submitted less than 1 H ago
    completed_1w_ago = [w for w in jobs_submitted_less_than_1w if BOINC_data["Job turnaround time"][w] < 604800]

    BOINC_data["1W submitted"].append(len(jobs_submitted_less_than_1w))


    # If no jobs have been completed in the past 1 H
    if completed_1w_ago == []:
        BOINC_data["1W completed"].append(0)
        BOINC_data["1W completed time avg"].append(0)
    else:
        BOINC_data["1W completed"].append(len(completed_1w_ago)/len(jobs_submitted_less_than_1w))
        BOINC_data["1W completed time avg"].append(np.mean([BOINC_data["Job turnaround time"][zi] for zi in completed_1w_ago]))






    if (qq % 10000) == 0:
        print(timformat(BOINC_data["Created time"][-1]))




# Computes the datetimes in strings as well for easier 
BOINC_data["dt YMD str"] = [timformat(dt_given) for dt_given in BOINC_data["Created time"]]


with open("boinc_data/preprocessed.pckl", "wb") as pf:
    pickle.dump(BOINC_data, pf)


"""


# Loads the BOINC data
with open("boinc_data/preprocessed.pckl", "rb") as datafile:
    BOINC_data = pickle.load(datafile)



##########################
# Functions to compute
# All have an input j, equal to the position in the BOINC dictionary array to search
# 
##########################

print("-------------------------")
print()



def hosts_available_in_this_date(j):
    return Host_data["hosts per day"][BOINC_data["dt YMD str"][j]]



def hosts_joined_in_this_date(j):
    return Host_data["hosts joined per day"][BOINC_data["dt YMD str"][j]]



def cpu_time(j):
    return BOINC_data["CPU time"][j]



def sq_cpu_time(j):
    return BOINC_data["CPU time"][j]**2



# 1 for wokdays, 0 for not: workdays are Monday, Tuesday, Wednesday, Thursday, Friday
def workday_or_not(j):
    wday = BOINC_data["Created time"][j].weekday()

    if wday < 5:
        return True
    else:
        return False



# 1 for workhours, 0 for not: workhours are defined as those between 13:00 and 23:00 UTC
# these correspond to 8:00-18:00 during summer daylight time
def workhours_or_not(j):
    whours = BOINC_data["Created time"][j].hour

    if (whours > 13) and (whours < 23):
        return True
    else:
        return False



# Computes how useful these  hours are using sine function
def cardiac_whours(j):

    whours = BOINC_data["Created time"][j].hour 
    val1 = math.sin((whours-13)*math.pi/10)
    return np.sign(val1)*abs(val1)**0.5


# 1 for day, 0 for night
# Day defined between 01:00 and 15:00 UTC
def day_or_night(j):
    whours = BOINC_data["Created time"][j].hour

    if (whours > 0) and (whours < 15):
        return True
    else:
        return False



def submitted_4h(j):
    return BOINC_data["4H submitted"][j]



def completed_4h(j):
    return BOINC_data["4H completed"][j]



# Completed in 4 h time avg
def completed_4h_time_avg(j):
    return BOINC_data["4H completed time avg"][j]




def submitted_1h(j):
    return BOINC_data["1H submitted"][j]



def completed_1h(j):
    return BOINC_data["1H completed"][j]



def completed_1h_time_avg(j):
    return BOINC_data["1H completed time avg"][j]




def submitted_1w(j):
    return BOINC_data["1W submitted"][j]



def completed_1w(j):
    return BOINC_data["1W completed"][j]



# Completed in 4 h time avg
def completed_1w_time_avg(j):
    return BOINC_data["1W completed time avg"][j]



# Constant: 1
def constant_C(j):
    return 1



used_functions = [hosts_available_in_this_date, workday_or_not, cardiac_whours, 
                submitted_1h, completed_1h, completed_1h_time_avg,
                submitted_4h, completed_4h, completed_4h_time_avg,
                submitted_1w, completed_1w, completed_1w_time_avg, constant_C]

number_of_completed_jobs = len(BOINC_data["CPU time"])



# Given two functions: F1, F2
# Returns the sum over all the data 
def sum_ls(F1, F2):
    return sum([F1(i)*F2(i) for i in range(0, number_of_completed_jobs)])


# Given a function: F
# Returns the sum of the multiplication of it by the expected value y_i
def result_member(F, y_results):
    return sum([F(i)*y_results[i] for i in range(0, number_of_completed_jobs)])



##########################
# ML keras
# 
##########################

print("\n-------------------------")
print("ML (keras) Results:")


# Reproducible seed
np.random.seed(0)




print("\n[-> triple job timer classifier]")


# Using the same data as before
"""
used_functions = [hosts_available_in_this_date, workday_or_not, 
                    cardiac_whours, submitted_4h, completed_4h, completed_4h_time_avg, constant_C]
"""

used_functions = [
                hosts_available_in_this_date,
                workday_or_not,
                cardiac_whours,
                submitted_4h,
                completed_4h,
                completed_4h_time_avg,
                submitted_1w,
                completed_1w,
                completed_1w_time_avg
                ]


data_matrix = np.zeros((number_of_completed_jobs, len(used_functions)+3))

for row in range(0, number_of_completed_jobs):
    for g in range(0, len(used_functions)):
        F = used_functions[g]

        data_matrix[row][g] = F(row)

    # Job will take longer than 1 h
    if BOINC_data["Job turnaround time"][row] < 1*3600:
        data_matrix[row][g+1] = 1
    elif BOINC_data["Job turnaround time"][row] > 12*3600:
        data_matrix[row][g+3] = 1
    else:
        # Between 1h and 12h
        data_matrix[row][g+2] = 1







# Divides the data into training and actual
training_portion = 0.90 # 90% of the data will be used for training


numbered_rows = list(range(0, number_of_completed_jobs))
# Fixes the seed
random.Random(0).shuffle(numbered_rows)

training_data = []
validation_data = []

cou = 0
for one_row in numbered_rows:

    if cou < training_portion*number_of_completed_jobs:
        training_data.append(data_matrix[one_row])
    else:
       validation_data.append(data_matrix[one_row]) 
    cou += 1


training_data = np.array(training_data)
validation_data = np.array(validation_data)



# Split into x, y variables
XT = training_data[:, 0:len(used_functions)]
YT = training_data[:, len(used_functions):]

XV = validation_data[:, 0:len(used_functions)]
YV = validation_data[:, len(used_functions):]


# Creates model
model = Sequential()
model.add(Dense(len(used_functions), input_dim=len(used_functions), kernel_initializer ='uniform', activation='linear'))
model.add(Dense(24, kernel_initializer ='uniform', activation='sigmoid'))
model.add(Dense(32, kernel_initializer ='uniform', activation='relu'))
model.add(Dense(24, kernel_initializer ='uniform', activation='relu'))
model.add(Dense(18, kernel_initializer ='uniform', activation='relu'))
model.add(Dense(16, kernel_initializer ='uniform', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(data_matrix[-1])-len(used_functions), kernel_initializer ='uniform', activation='softmax'))

# Compiles the model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
# Fit the model
model.fit(XT, YT, epochs=70, batch_size=10000,  verbose=0)

scores = model.evaluate(XV, YV)
model.save('boinc_3classifier.h5')
print("\nValidation data (%s): %.2f%%" % (model.metrics_names[1], scores[1]*100))

predictions = model.predict(XV)

print(predictions)


print(sf.precission_classifier(YV, predictions))



