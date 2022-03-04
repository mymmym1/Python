# This implementation is very slow
def editDistRecursive(x, y):
    if len(x) == 0:
        return len(y)
    elif len(y) == 0:
        return len(x)
    else:
        distHor = editDistRecursive(x[:-1], y) + 1
        distVer = editDistRecursive(x, y[:-1]) + 1
        if x[-1] == y[-1]:
            distDiag = editDistRecursive(x[:-1], y[:-1])
        else:
            distDiag = editDistRecursive(x[:-1], y[:-1]) + 1
        return min(distHor, distVer, distDiag)
# Matrix is faster
def editDistance(x, y):
    # Create distance matrix
    D = []
    for i in range(len(x)+1):  # add one empty string column and row
        D.append([0]*(len(y)+1))  # Initialize list length
    # Initialize first column and row of matrix
    for i in range(len(x)+1):
        D[i][0] = i  # Initialize the first row and column values = a, b base numbers
    for i in range(len(y)+1):
        D[0][i] = i
    # Fill in the rest of the matrix
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            distHor = D[i][j-1] + 1
            distVer = D[i-1][j] + 1
            if x[i-1] == y[j-1]:
                distDiag = D[i-1][j-1]
            else:
                distDiag = D[i-1][j-1] + 1
            D[i][j] = min(distHor, distVer, distDiag)
    # So far we don't know the value in each position until we fill them with 2 sequences' comparison result
    return D[-1][-1]  # Edit distance is the value in the bottom right corner of the matrix

x = 'shake spea'
y = 'Shakespear'
# print(editDistRecursive(x, y))
# print(editDistance(x, y))

### hw3 ###
def editDistancePinT(x, y):
    D = []
    for i in range(len(x)+1):  # Initialize matrix
        D.append([0]*(len(y)+1))
    for i in range(len(x)+1):
        D[i][0] = i  # Initialize the first column values = the number of x index
    for i in range(len(y)+1):
        D[0][i] = 0   # Initialize first row values = 0, because we don't know where p happens in T
    # Fill in the rest of the matrix
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            distHor = D[i][j-1] + 1
            distVer = D[i-1][j] + 1
            if x[i-1] == y[j-1]:
                distDiag = D[i-1][j-1]
            else:
                distDiag = D[i-1][j-1] + 1
            D[i][j] = min(distHor, distVer, distDiag)
    # So far we don't know the value in each position until we fill them with 2 sequences' comparison result
    return min(D[-1])  # Edit distance is the min value in the last row of the matrix

def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome
humanChrom1_sequences = readGenome('chr1GRCh38excerpt.fasta')

p1 = 'GCTGATCGATCGTACG'
p2 = 'GATTTACCAGATTGAG'
# print(editDistancePinT(p1, humanChrom1_sequences))
print(editDistancePinT(p2, humanChrom1_sequences))
