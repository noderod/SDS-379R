"""
BASICS

Reads the JSON file with Stampede2 job data
Presents it in a suitable form
"""



import json
import matplotlib.pyplot as plt
import numpy as np



with open ("stampede2_results.json", "r") as jf:
    S2_data = json.load(jf)



appnames = ["AutoDock Vina", "Bedtools", "Blast", "Bowtie", "Gromacs", "HTSeq", "MPI-LAMMPS", "NAMD", "OpenSees"]
possible_colors = ["k", "r", "g", "b", "m", "c", "darkorange", "gray", "gold"]
cou = 1



# Runtime


plt.figure()

for app, cc in zip(appnames, possible_colors):

    print(app+": ")
    print("Avg. runtime: "+str(np.mean(S2_data[app]["runtime"]))+" s")
    print("Std. runtime: "+str(np.std(S2_data[app]["runtime"]))+" s")
    print("\n")

    plt.plot(len(S2_data[app]["runtime"])*[cou], S2_data[app]["runtime"], 'o', color=cc,label=app)

    cou += 1

plt.xticks(list(range(1, 1+len(appnames))), appnames)
plt.xlabel("Application name")
plt.ylabel("Runtime (s)")
plt.title("Runtime per application")
plt.legend()



cou = 1
# Job turn-around time
plt.figure()

for app, cc in zip(appnames, possible_colors):

    print(app+": ")
    print("Avg. job turn-around time: "+str(np.mean(S2_data[app]["complete_time"]))+" s")
    print("Std. job turn-around time: "+str(np.std(S2_data[app]["complete_time"]))+" s")
    print("\n")

    plt.plot(len(S2_data[app]["complete_time"])*[cou], S2_data[app]["complete_time"], 'o', color=cc,label=app)

    cou += 1

plt.xticks(list(range(1, 1+len(appnames))), appnames)
plt.xlabel("Application name")
plt.ylabel("Job turn-around time (s)")
plt.title("Job turn-around time per application")
plt.legend()







plt.show()

