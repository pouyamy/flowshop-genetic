import random

def arbitrary_three_job(individual):
    # Step 1: Select three random elements
    selected_elements = random.sample(individual, 3)

    # Step 2: extract indices of random elements to change the elements
    indices = [individual.index(i) for i in selected_elements]  

    # Step 3: replace selected jobs at random locations amongst the selected jobs
    random.shuffle(indices)
    # randomly change selected jobs between selected elements
    for idx in indices:
        job = random.choice(selected_elements)
        selected_elements.remove(job)
        individual[idx] = job
        
    return individual

def arbitrary_two_job(individual):
    # Step 1: Select two random elements
    selected_elements = random.sample(individual, 2)

    # Step 2: Extract indices of random elements to change the elements
    idx1, idx2 = [individual.index(i) for i in selected_elements] 

    # Step 3: Interchange selected elements in an individual
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    return individual

def shift_change(individual):
    # Step 1: Select an element 
    selected_element = random.choice(individual)

    # Step 2: Select a position to insert the selected job
    selected_position = random.choice([individual.index(i) for i in individual if i != selected_element])

    # Step 3: remove selected job from its current position and insert it on the new position
    individual.remove(selected_element)
    individual.insert(selected_position, selected_element)
    
    return individual