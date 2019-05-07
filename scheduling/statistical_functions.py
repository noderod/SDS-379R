"""
BASICS

Statistical functions
"""


import numpy as np
import numpy.linalg as LA




# Computes the R square between two arrays: original and fitted
# original_arr, fitted_arr (arr)

def R2(original_arr, fitted_arr):

    y_avg = np.mean(original_arr)
    SS_tot = sum([(y - y_avg)**2 for y in original_arr ])
    SS_res = sum([(y_i - f_i)**2 for y_i, f_i in zip(original_arr, fitted_arr)])

    return 1 - SS_res/SS_tot



# Computes the RMS
def RMS_error(original_arr, fitted_arr):

    ecalc = np.array(original_arr) - np.array(fitted_arr)
    return (np.mean([x**2 for x in ecalc])  )**0.5



# Computes the RMS relative error
def RMS_rel_error(original_arr, fitted_arr):

    rel_ecalc = [(x1-x2)/x1 for x1, x2 in zip(original_arr, fitted_arr)]
    return (np.mean([x**2 for x in rel_ecalc])  )**0.5


# Computes the precision, recall of a 1D keras model
# keras_model (keras model)
# y_original (ND array)
# y_computed (ND array)
def precission_classifier(y_original, y_computed):

    correct_class = np.zeros(len(y_original[0]))

    orig_class = [list(y).index(max(y)) for y in y_original]
    comp_class = [list(y).index(max(y)) for y in y_computed]

    for datatype in range(0, len(correct_class)):

        for origloc, comploc in zip(orig_class, comp_class):

            if origloc != datatype:
                continue

            if origloc == comploc:
                correct_class[datatype] += 1

        correct_class[datatype] /= len([orig for orig in orig_class if orig == datatype])

    return [correct_class]




##############
# Least-Squares functions
##############

# Given two functions: F1, F2
# Returns the sum over all the data 
def sum_ls(F1, F2, number_of_completed_jobs):
    return sum([F1(i)*F2(i) for i in range(0, number_of_completed_jobs)])


# Given a function: F
# Returns the sum of the multiplication of it by the expected value y_i
def result_member(F, y_results):
    number_of_completed_jobs = len(y_results)
    return sum([F(i)*y_results[i] for i in range(0, number_of_completed_jobs)])


# Solves the coefficients (a) of a linear system using numpy's builtin Gauss' method
def gauss_solve(used_functions, y_empirical):

    # Result matrix, 1D array because it is in LA.solve form
    #Y = [result_member(f, BOINC_data["Job turnaround time"]) for f in used_functions]

    Y = [result_member(f, y_empirical) for f in used_functions]
    X = np.zeros((len(used_functions), len(used_functions)))

    n_jobs_completed = len(y_empirical)

    for row in range(0, len(used_functions)):
        for col in range(0, len(used_functions)):
            X[row][col] = sum_ls(used_functions[row], used_functions[col], n_jobs_completed)

    # Solves for the coefficients
    a = LA.solve(X, Y)
    return a



def fitted_result(Betas, functions, x_original):

    YF = []
    lf = len(Betas)

    for xi in x_original:
        YF.append(sum([Betas[k]*functions[k](xi) for k in range(0, lf)]))

    return YF




