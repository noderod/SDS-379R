"""
BASICS

Provides some basic statistics about user and hosts
"""


import datetime
import json
import matplotlib.pyplot as plt
from scipy import stats






# Obtains the day given a certain Unix timestamp
# Date is in format YYYY-MM-DD (str)
# unix_timestamp (int)
def YYYYMMDD_from_unix_timestamp(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d')




with open("users_hosts.json", "r") as datafile:
    RAW_DATA = json.load(datafile)




#####################
# Join dates
#####################


# Gets all joined dates
users_unix_joined_times = RAW_DATA["users"]["join time"]
hosts_unix_joined_times = RAW_DATA["hosts"]["join time"]

users_join_better_dates = [YYYYMMDD_from_unix_timestamp(float(x)) for x in users_unix_joined_times]
hosts_join_better_dates = [YYYYMMDD_from_unix_timestamp(float(x)) for x in hosts_unix_joined_times]

first_day = datetime.datetime.strptime(users_join_better_dates[0], "%Y-%m-%d")
last_day = datetime.datetime.strptime(users_join_better_dates[-1], "%Y-%m-%d")
delta = last_day - first_day

actual_dates = []


# Finds which users joined in what date

users_joined_in_this_date = []
hosts_joined_in_this_date = []

for qq in range(delta.days + 1):
    actual_dates.append((first_day + datetime.timedelta(qq)).strftime("%Y-%m-%d"))

    users_joined_in_this_date.append(users_join_better_dates.count(actual_dates[-1]))
    hosts_joined_in_this_date.append(hosts_join_better_dates.count(actual_dates[-1]))




# Finds the cumulative number of users and hosts
users_per_day = [users_joined_in_this_date[0]]
hosts_per_day = [hosts_joined_in_this_date[1]]
for new_date in actual_dates[1::]:
	users_per_day.append(users_per_day[-1]+users_join_better_dates.count(new_date))
	hosts_per_day.append(hosts_per_day[-1]+hosts_join_better_dates.count(new_date))



D1 = {"hosts per day":{}, "hosts joined per day":{}}

# Dictionaries with hosts and hosts joined per day
for new_date, cou in zip(actual_dates, range(0, len(actual_dates))):
    D1["hosts per day"][new_date] = hosts_per_day[cou]
    D1["hosts joined per day"][new_date] = hosts_joined_in_this_date[cou]




# Writes the result to a file with dates for easier parsing later
with open("hosts_per_day.json", "w") as jf:
    jf.write(json.dumps(D1))



#####################
# Plots
#####################




plt.figure()
plt.plot(users_per_day, "r-", label="Volunteers")
plt.plot(hosts_per_day, "g-", label="Volunteer devices")

plt.xlabel("Date")
plt.ylabel("Number")
plt.xticks([0, 25, 56, len(actual_dates)-1], [actual_dates[0], actual_dates[25], actual_dates[56], actual_dates[-1]])
plt.title("Volunteers, devices per day vs. Date")
plt.legend()


plt.figure()
plt.plot(users_joined_in_this_date, "r--", label="Volunteers")
plt.plot(hosts_joined_in_this_date, "g--", label="Volunteer devices attached")

plt.xlabel("Date")
plt.ylabel("Number joined per per day")
plt.xticks([0, 25, 56, len(actual_dates)-1], [actual_dates[0], actual_dates[25], actual_dates[56], actual_dates[-1]])
plt.title("Volunteers, devices attached per day vs. Date")
plt.legend()



#####################
# How many hosts each user has
#####################


users_ids = RAW_DATA["users"]["id"]
hosts_user_id = RAW_DATA["hosts"]["user id"]


hosts_per_user = []

for usid in users_ids:
	hosts_per_user.append(hosts_user_id.count(usid))


# How many users have x number of systems
hosts_number = [z for z in set(hosts_per_user)]
n_users_with_x_hosts = [hosts_per_user.count(s) for s in hosts_number]


plt.figure()
bar1 = plt.bar(hosts_number, n_users_with_x_hosts, color='blue', alpha=0.6)


# Adds text on top of them
for rect in bar1:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')


plt.yscale('log')
plt.xticks(hosts_number)
plt.yticks([0.8, 1, 10, 100, 1000], [0.8, 1, 10, 100, 1000])

plt.xlabel("Attached volunteer devices")
plt.ylabel("Number of volunteers")
plt.title("Volunteers per number of associated volunteer devices")



plt.show()
