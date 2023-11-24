import numpy as np
import math

def dtw(seq1, seq2):    
    # Create the cost matrix.
    cost = np.zeros((len(seq1), len(seq2)))
    cost[0, 0] = abs(seq1[0] - seq2[0])
    for i in range(1, len(seq1)):
        cost[i, 0] = cost[i - 1, 0] + abs(seq1[i] - seq2[0])
    for j in range(1, len(seq2)):
        cost[0, j] = cost[0, j - 1] + abs(seq1[0] - seq2[j])
    
    # Fill in the rest of the cost matrix.
    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):
            cost[i, j] = min(cost[i - 1, j], cost[i, j - 1], cost[i - 1, j - 1]) + abs(seq1[i] - seq2[j])
    
    # Return the DTW distance.
    return cost[-1, -1]

def utw(seq1, seq2):
    cost = 0
    l = len(seq1) * len(seq2)
    for i in range(1, l-1):
        cost += pow(seq1[math.floor(i/len(seq2))] - seq2[math.floor(i/len(seq1))], 2)
    return cost/l

seq1 = [1, 2, 3, 4, 7]
seq2 = [2,4,7]

print(dtw(seq1, seq2))
print(utw(seq1, seq2))