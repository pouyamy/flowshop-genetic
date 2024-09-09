# Improved Genetic Algorithm for Flowshop Scheduling Problem - Re-implementation

This repository contains a re-implementation of the paper:  
**An improved genetic algorithm for the flowshop scheduling problem**, published in the *International Journal of Production Research*, 2007.  
[DOI: 10.1080/00207540701523041](https://doi.org/10.1080/00207540701523041)

## Overview

The Flowshop Scheduling Problem (FSP) is a classic optimization problem in production scheduling. The goal is to determine the optimal sequence of jobs to minimize the overall completion time (makespan) in a flowshop environment, where jobs pass through multiple machines in the same order.

This repository implements the improved genetic algorithm (GA) described in the paper, which enhances the standard GA by introducing techniques such as multi-crossover operators, multi-mutation operators and hypermutation to achieve better performance in solving the FSP.

## Key Features

- **Improved Genetic Algorithm**: Implementation of the enhanced GA with multi-crossover operators, multi-mutation operators and hypermutation, as proposed in the paper.
- **Performance-Oriented**: Focuses on minimizing makespan in flowshop environments, which is critical in manufacturing and production scheduling.
- **Modular Design**: The code is structured into modules for easier understanding and adaptability.

- ## Problem Formulation

The goal of the flowshop scheduling problem is to minimize the makespan (the time it takes to complete all jobs) while adhering to the following conditions:
- \( m \) machines and \( n \) jobs.
- Each job \( J_i \) must be processed on each machine \( M_j \) in the same order.
- The objective is to find the sequence of jobs that minimizes the total makespan.

- ## References
- Rajkumar, R., & Shahabudeen, P. (2008). An improved genetic algorithm for the flowshop scheduling problem. International Journal of Production Research, 47(1), 233–249. https://doi.org/10.1080/00207540701523041
