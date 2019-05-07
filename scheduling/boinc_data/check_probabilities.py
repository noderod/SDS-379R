"""
BASICS

Checks probabilities of the different things
"""


import pickle



# Loads the BOINC data
with open("preprocessed.pckl", "rb") as datafile:
    BOINC_data = pickle.load(datafile)



CT = BOINC_data["Job turnaround time"]


population_size = len(CT)

def percentage_prob(x):
    return 100*len(x)/population_size


print("< 1h: "+str(percentage_prob( [y for y in CT if y < 1*3600] ))+" %")
print("[1h, 12h): "+str(percentage_prob( [y for y in CT if (y >= 1*3600) and (y <= 12*3600)] ))+" %")
print("> 12h: "+str(percentage_prob( [y for y in CT if y > 12*3600] ))+" %")
