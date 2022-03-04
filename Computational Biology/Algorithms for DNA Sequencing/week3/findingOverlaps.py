from itertools import permutations

def overlap(a, b, min_length=3):
    """ Return [length of longest suffix of 'a'] matching
        a [prefix of 'b'] that is at [least 'min_length']
        characters long.  If no such overlap exists,
        return 0. """
    start = 0  # search start from index = 0 of a
    while True:
        #  Syntax: string.find(value, start, end)
        start = a.find(b[:min_length], start)  # look for b's prefix (min_length) in whole a, everytime return the 1st index found
        if start == -1:  # no occurrence found (e.g. when a gets too short and no b[:min_length] found)
            return 0  # get over overlap() function, no overlap found
        # when the left->right 1st overlap index (start) is found, check for full suffix/prefix match
        if b.startswith(a[start:]):  # if a[start:] including lots of bases don't belong to b.startswith, go to start += 1 and look for the next 1st index found
            return len(a)-start  # return the max length of overlap
        start += 1

# print(overlap('TTACGT', 'CGTGTGC'))
# print(overlap('TTACGT', 'GTGTGC'))  # only 2 overlaps < min_length=3, return 0

# print(list(permutations([1,2,3],2)))
'''
def naive_overlap_map(reads, k):  # k = min_length of overlap. reads: a list of sequences
    olaps = {}  # dictionary {(a,b):maxOverlapLen, ...}
    for a, b in permutations(reads, 2):  # compare each 2 reads
        maxOverlapLen = overlap(a, b, min_length=k)  # This is slow
        if maxOverlapLen > 0:
            olaps[(a, b)] = maxOverlapLen
    return olaps

reads = ['ACGGATC', 'GATCAAGT', 'TTCACGGA']
# print(naive_overlap_map(reads, 3))
'''
### hw3 ###
def readFastq(filename):
    sequences = []  # String list
    qualities = []
    with open (filename) as fh:
        while True:
            fh.readline()  # read the first line which is a tag
            seq = fh.readline().rstrip()  # read the second line which is DNA sequence
            fh.readline()  # read the 3rd line
            qual = fh.readline().rstrip()
            if len(seq) == 0:  # String length
                break
            sequences.append(seq)
            qualities.append(qual)
    return sequences, qualities
phix_sequences, _ = readFastq('ERR266411_1.for_asm.fastq')

def naive_overlap_map_faster(reads, k):  # k = min_length of overlap. reads: a list of sequences
    dic = {}
    for r in reads:
        kmerSet = set()
        for i in range(len(r) - k + 1):
            kmerSet.add(r[i:i + k])
        for kmer in kmerSet:
            if not kmer in dic.keys():
                dic[kmer] = set()
            dic[kmer].add(r)
    olaps = {}  # dictionary {(r,r2):maxOverlapLen, ...}
    # try not call overlap if r doesn't contain r2's kmer suffix
    for r in reads:
        for r2 in dic[r[-k:]]:
            if r != r2:
                maxOverlapLen = overlap(r, r2, min_length=k)  # This is slow
                if maxOverlapLen > 0:
                    olaps[(r, r2)] = maxOverlapLen
    nodeSet = set()
    for s in olaps.keys():
        nodeSet.add(s[0])
    numNodes = len(nodeSet)
    return olaps, numNodes

olaps, numNodes = naive_overlap_map_faster(phix_sequences, 30)
edges = len(olaps)
print(edges)  # 904746
print(numNodes)  # 7161

# reads = ['ABCDEFG', 'EFGHIJ', 'HIJABC']
# print(naive_overlap_map_faster(reads, 3))
# print(naive_overlap_map_faster(reads, 4))

# reads = ['CGTACG', 'TACGTA', 'GTACGT', 'ACGTAC', 'GTACGA', 'TACGAT']
# print(naive_overlap_map_faster(reads, 4))
# print(naive_overlap_map_faster(reads, 5))