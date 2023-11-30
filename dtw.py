import numpy as np
import math
#from fastdtw import fastdtw

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

def utw_norm(seq, w):
    #w-upsampling of a sequence
    norm_seq = []
    for i in range(0, len(seq)*w-1):
        norm_seq.append(seq[math.floor(i/w)])
    return norm_seq

def ldtw_constraint(seq1,seq2, i,j ,k):
    if abs(i-j) > k:
        return np.inf
    else:
        return abs(seq1[i] - seq2[j])
    
def ldtw(seq1, seq2, delta):
    norm_seq1 = utw_norm(seq1, math.ceil(len(seq2)/len(seq1)))
    norm_seq2 = utw_norm(seq2, math.ceil(len(seq1)/len(seq2)))
    # norm_seq1 = seq1
    # norm_seq2 = seq2   
    # l = math.lcm(len(seq1), len(seq2))
    # norm_seq1 = utw_norm(seq1, l)
    # norm_seq2 = utw_norm(seq2, l)
    
    k = (delta * len(seq1) -1)/2
    cost = np.zeros((len(norm_seq1), len(norm_seq2)))
    cost[0, 0] = ldtw_constraint(norm_seq1, norm_seq2, 0, 0, k)
    for i in range(1, len(norm_seq1)):
        cost[i, 0] = cost[i - 1, 0] + ldtw_constraint(norm_seq1, norm_seq2, i, 0, k)
    for j in range(1, len(norm_seq2)):
        cost[0, j] = cost[0, j - 1] +   ldtw_constraint(norm_seq1, norm_seq2, 0, j, k)
    
    for i in range(1, len(norm_seq1)):
        for j in range(1, len(norm_seq2)):
            cost[i, j] = min(cost[i - 1, j], cost[i, j - 1], cost[i - 1, j - 1]) + ldtw_constraint(norm_seq1, norm_seq2, i, j, k)
    
    #print the cost matrix
    # for i in range(0, len(norm_seq1)):
    #     for j in range(0, len(norm_seq2)):
    #         print(cost[i,j], end = ' ')
    #     print()
    return cost[-1, -1]
    
# def lb_Keogh(seq1,seq2,r):
#     #let seq1 be the query 
#     #let the seq2 be the match sequence
    
#     #distance,path = fastdtw(seq1,seq2)
    
#     U_Keogh = []
#     L_Keogh = []
#     for i in range(0,len(seq1)):
#         U_Keogh[i] = maxfn(seq1,i,r)
#         L_Keogh[i] = minfn(seq1,i,r)
    
#     cost = 0
#     l = min(len(seq1), len(seq2))
#     for i in range(0,l):
#         if (seq2[i]>U_Keogh[i]):
#             cost+=pow((seq2[i]-U_Keogh[i]),2)
#         if (seq2[i]<L_Keogh[i]):
#             cost+=pow((seq2[i]-L_Keogh[i]),2)
    
#     return math.sqrt(cost)
            
# def maxfn(seq,i,r):
#     max = 0
#     if(i-r<0):
        
                  
    
    
    



# seq1 = [1, 2, 3, 4, 7]
# seq2 = [2,4,7]

# print("DTW distance: " ,dtw(seq1, seq2))
# print("UTW Distance: " ,utw(seq1, seq2))
# print("LDTW Distance: ",ldtw(seq1, seq2, 0.05))