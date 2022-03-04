import collections
import matplotlib.pyplot as plt

def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome

genome = readGenome('lambda_virus.fa')
# print(genome[:100])

# counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
#for base in genome:
#    counts[base] += 1
# print(counts)

# print(collections.Counter(genome))

complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
def naive_with_rc(fragment, genome):
    matchIndices = []  # a list of the matching index in t
    for i in range(len(genome) - len(fragment) + 1):  # Loop over alignments
        match = True
        for j in range(len(fragment)):
            if genome[i + j] != fragment[j]:
                match = False  # if True, keep on this for loop, not go to the next if
                break  # stop this for loop
        if match:
            matchIndices.append(i)  # only i: the matching index in t; Then go to the next i of the outer for loop
        else:
            match = True
            for j in range(len(fragment)):
                if genome[i + j] != complement[fragment[j]]:
                    match = False
                    break
            if match:
                matchIndices.append(i)  # only i: the matching index in t; Go to the next i of the outer for loop
    return matchIndices

def naive(p, t):  # p: fragment, t: genome
    matchIndices = []  # a list of the matching index in t
    for i in range(len(t) - len(p) + 1):  # Loop over alignments
        match = True
        for j in range(len(p)):
            if t[i + j] != p[j]:  # can also be written: if not t[i + j] == p[j]:
                match = False  # if True, keep on this for loop, not go to the next if
                break  # break this for loop and go to the first for loop
        if match:
            matchIndices.append(i)  # only i: the matching index in t; Go to the next i of the outer for loop
    return matchIndices

p = 'CCC'
ten_as = 'AAAAAAAAAA'
t = ten_as + 'CCC' + ten_as + 'GGG' + ten_as
occurrences = naive_with_rc(p, t)
# print(occurrences)
# occurrences = naive(p, t)
# print(occurrences)

matchIndices = naive_with_rc('AGTCGA', genome)
# print('offset of leftmost occurrence: %d' % min(matchIndices))
# print('# occurrences: %d' % len(matchIndices))

# matchIndices = naive('ATTA', genome)
# print('# occurrences: %d' % len(matchIndices))

# Allow <= 2 mismatches without considering the complement DNA strand
def naive_2mm(p, t):  # p: fragment, t: genome
    matchIndices = []  # a list of the matching index in t
    for i in range(len(t) - len(p) + 1):  # Loop over alignments
        match = True
        numMismatch = 0
        for j in range(len(p)):
            if t[i + j] != p[j]:  # can also be written: if not t[i + j] == p[j]:
                numMismatch += 1
                if numMismatch > 2:
                    match = False  # if True, keep on this for loop, not go to the next if
                    break  # break this for loop and go to the first for loop
        if match:
            matchIndices.append(i)  # only i: the matching index in t; Go to the next i of the outer for loop
    return matchIndices

p = 'ACTTTA'
t = 'ACTTACTTGATAAAGT'
occurrences = naive_2mm(p, t)
# print(occurrences)
matchIndices = naive_2mm('AGGAGGTT', genome)
# print('offset of leftmost occurrence: %d' % min(matchIndices))
# print('# occurrences: %d' % len(matchIndices))

def phred33ToQ(qual):
    return ord(qual) - 33
def findMinQInd(filename):
    minIndices = []
    with open(filename) as fh:
        while True:
            fh.readline()  # read the first line which is a tag
            seqLine = fh.readline().rstrip()  # read the second line which is DNA sequence
            fh.readline()  # read the 3rd line
            qualLine = fh.readline().rstrip()
            #print(qualLine)
            if len(seqLine) == 0:  # String length
                break
            else:
                Q = [0] * len(qualLine)
                for i in range(len(qualLine)):
                    Q[i] = phred33ToQ(qualLine[i])
                #print(Q)
                for i in range(len(Q)):
                    if Q[i] == min(Q):
                        minIndices.append(i)
    # print(minIndices)
    minQIndCount = collections.Counter(minIndices)
    #print(minQIndCount)
    max_key = []
    for (k,v) in minQIndCount.items():
        if v == max(minQIndCount.values()):
            max_key.append(k)
    return max_key

max_key = findMinQInd('ERR037900_1.first1000.fastq')
print(max_key)
