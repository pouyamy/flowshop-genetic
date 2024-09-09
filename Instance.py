import numpy as np
import pandas as pd

def read_instance(filename):   
    jobs = {}
    n_jobs = 0
    n_machines = 0
    with open(filename, "r") as file:
        #  Read number of jobs and machines
        line = file.readline()
        n_jobs = int(line.split()[0])
        n_machines = int(line.split()[1])
        # Parsing processing time information of machines for each job
        for j in range(n_jobs):
            jobs[j] = {}
            line = file.readline()
            fields = line.split()
            for m in range(0, len(fields), 2):
                jobs[j][int(fields[m])] = int(fields[m + 1])
    
    # Extracting column
    columns = sorted(set(key for sub_dict in jobs.values() for key in sub_dict))

    # Creating an empty matrix to store P_ij
    num_rows = len(jobs)
    num_cols = len(columns)
    p_ij = np.zeros((num_rows, num_cols))

    # Filling the P_ij with values from the nested dictionary
    for i, (row_key, row_dict) in enumerate(jobs.items()):
        for j, col_key in enumerate(columns):
            p_ij[i, j] = row_dict.get(col_key, 0)
              
    return jobs, p_ij.T, n_jobs, n_machines

def read_excel(excel_path):
    df = pd.read_excel(excel_path, header= None)
    p_ij = df.to_numpy()
    n_machines = len(p_ij)
    n_jobs = len(p_ij[0])
    jobs = df.to_dict()
    
    return jobs, p_ij, n_jobs, n_machines