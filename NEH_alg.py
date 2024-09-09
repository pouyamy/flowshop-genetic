import numpy as np

# Calculate completion Time for each Job on each Machine.
def completion_time(my_seq, p_ij, nbm):
    c_ij = np.zeros((nbm, len(my_seq) + 1))

    for j in range(1, len(my_seq) + 1):
        c_ij[0][j] = c_ij[0][j - 1] + p_ij[0][my_seq[j - 1]]

    for i in range(1, nbm):
        for j in range(1, len(my_seq) + 1):
            c_ij[i][j] = max(c_ij[i - 1][j], c_ij[i][j - 1]) + p_ij[i][my_seq[j - 1]]
    return c_ij

# Calculate Sum Processing Time
def sum_processing_time(index_job, p_ij, nb_machines):
    sum_p = 0
    for i in range(nb_machines):
        sum_p += p_ij[i][index_job]
    return sum_p

# Detect NEH Order
def order_neh(p_ij, nb_machines, nb_jobs):
    my_seq = []
    for j in range(nb_jobs):
        my_seq.append(j)
    return sorted(my_seq, key=lambda x: sum_processing_time(x, p_ij, nb_machines), reverse=True)

# Put new job into the sequence
def insertion(sequence, index_position, value):
    new_seq = sequence[:]
    new_seq.insert(index_position, value)
    return new_seq

# NEH Heuristic Solution
def neh(p_ij, nb_machines, nb_jobs):
    order_seq = order_neh(p_ij, nb_machines, nb_jobs)
    seq_current = [order_seq[0]]
    for i in range(1, nb_jobs):
        min_cmax = float("inf")
        for j in range(0, i + 1):
            tmp_seq = insertion(seq_current, j, order_seq[i])
            cmax_tmp = completion_time(tmp_seq, p_ij, nb_machines)[nb_machines - 1][len(tmp_seq)]
            if min_cmax > cmax_tmp:
                best_seq = tmp_seq
                min_cmax = cmax_tmp
        seq_current = best_seq
    return seq_current, completion_time(seq_current, p_ij, nb_machines)[nb_machines - 1][nb_jobs]