import random
from collections import Counter

def two_points_crossover(parent_A, parent_B):

    size = len(parent_A)
    
    # Step 1: Two points are randomly selected for dividing the parents
    crossover_point1, crossover_point2 = sorted(random.sample(range(1, size - 1), 2))
    
    # Step 2: The jobs outside the selected two points are directly inherited from the parent A
    child_tmp = parent_A[:crossover_point1] + parent_A[crossover_point2:]
    # Step 3: The remaining elements in the child are filled by scanning parent B
    not_in_child_tmp = [gene for gene in parent_B if gene not in child_tmp]
    child_A = parent_A[:crossover_point1] + not_in_child_tmp + parent_A[crossover_point2:]

    # Step 2: The jobs outside the selected two points are directly inherited from the parent B
    child_tmp = parent_B[:crossover_point1] + parent_B[crossover_point2:]
    # Step 3: The remaining elements in the child are filled by scanning parent A
    not_in_child_tmp = [gene for gene in parent_A if gene not in child_tmp]
    child_B = parent_B[:crossover_point1] + not_in_child_tmp + parent_B[crossover_point2:]

    return child_A, child_B

def partially_mapped_crossover(parent_A, parent_B):
    
    size = len(parent_A)
    
    # Step 1: Two points are randomly selected for dividing the parents
    point1, point2 = sorted(random.sample(range(1, size - 1), 2))
    
    # Step 2: Exchanges the mapping section of the parent to the child
    child_A = parent_B[point1:point2]
    # Step 3: Define one-to-one mapping between genes of mapping section
    mapping = {parent_B[i]: parent_A[i] for i in range(point1, point2)}
    for i in range(size):
        if i < point1 or i > point2 - 1:
            gene = parent_A[i]
            while gene in mapping.keys():
                gene = mapping[gene]
            child_A.insert(i, gene)

    # Step 2: Exchanges the mapping section of the parent to the child
    child_B = parent_A[point1:point2]
    # Step 3: Define one-to-one mapping between genes of mapping section
    mapping = {parent_A[i]: parent_B[i] for i in range(point1, point2)}
    for i in range(size):
        if i < point1 or i > point2 - 1:
            gene = parent_B[i]
            while gene in mapping.keys():
                gene = mapping[gene]
            child_B.insert(i, gene)
    
    return child_A, child_B

def similar_job_order_crossover(parent_A, parent_B):
    
    # Determine the crossover point
    crossover_point = random.randint(1, len(parent_A) - 1)
    
    # Create copies of parents with None elements
    child_A = [None]*len(parent_A)
    child_B = [None]*len(parent_B)

    # Step 1: Detect identical jobs at the same positions
    zipped_parent = list(zip(parent_A, parent_B))
    for idx, (value_a, value_b) in enumerate(zipped_parent):
        if value_a == value_b:
            child_A[idx] = value_a
            child_B[idx] = value_b

    # Step 2: The child directly inherits all jobs from the corresponding parents up to a randomly chosen cut point
    for i in range(crossover_point):
        job1 = parent_A[i]
        job2 = parent_B[i]
        child_A[i] = job1
        child_B[i] = job2

    # Step 3: Missing elements at each Child are copied in the relative order of the other parent
    order = 0
    missing_child_A = [gene for gene in parent_B if gene not in child_A]
    missing_child_B = [gene for gene in parent_A if gene not in child_B]
    for idx, j in enumerate(child_A):
        if j == None:
            child_A[idx] = missing_child_A[order]
            order += 1

    order = 0
    for idx, j in enumerate(child_B):
        if j == None:
            child_B[idx] = missing_child_B[order]
            order += 1
    
    return child_A, child_B

def linear_order_crossover(parent_A, parent_B):
    # Step 1: Select a subsequence of operations from one parent at random
    point1, point2 = sorted(random.sample(range(1, len(parent_A) - 1), 2))
    child_A = [None]*len(parent_A)
    child_B = [None]*len(parent_B)

    # Step 2: Produce a proto-offspring by copying the subsection sequence into the corresponding positions of it
    for i in range(len(parent_A)):
        if i >= point1 and i < point2:
            child_A[i] = parent_A[i]
    
    # Step 3: Delete the operations which are already in the subsequence from the second parent.
    child_A_remove = parent_A[point1:point2]
    counter_to_remove = Counter(child_A_remove)
    child_B_filtered = [j for j in parent_B if counter_to_remove[j] == 0]

    # Step 4: Place the operations into the unfixed positions of the proto-offspring from left to right according to the order of the sequence to produce an offspring.
    order = 0
    for idx, j in enumerate(child_A):
        if j == None:
            child_A[idx] = child_B_filtered[order]
            order += 1

    for i in range(len(parent_B)):
        if i >= point1 and i < point2:
            child_B[i] = parent_B[i]

    child_B_remove = parent_B[point1:point2]
    counter_to_remove = Counter(child_B_remove)
    child_A_filtered = [j for j in parent_A if counter_to_remove[j] == 0]

    order = 0
    for idx, j in enumerate(child_B):
        if j == None:
            child_B[idx] = child_A_filtered[order]
            order += 1
    
    return child_A, child_B