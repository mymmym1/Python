from itertools import permutations

def overlap(a, b, min_length=2):
    """ Return length of longest [suffix of 'a'] matching
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

# Brute force method (may overcollapsing repeats)
def scs(ss):  # ss is the string list
    """ Returns shortest common superstring of given strings,
        assuming no string is a strict substring of another """
    ### hw4 ###
    # shortest_sup = None
    shortest_sup = set()
    ###
    for ssperm in permutations(ss):  # every possible orders of the reads, ssperm is one kind of string list
        sup = ssperm[0]  # first string of the string list
        for i in range(len(ss)-1):
            olen = overlap(ssperm[i], ssperm[i+1], min_length=1)
            sup += ssperm[i+1][olen:]  # The part before [olen:] of ssperm[i+1] overlaps with ssperm[i]
        ### hw4 ###
        # if shortest_sup is None or len(sup) < len(shortest_sup):
        if len(shortest_sup) == 0 or len(sup) < len((list(shortest_sup))[0]):
            shortest_sup = set()
            shortest_sup.add(sup)
            # shortest_sup = sup  # just get the shortest one
        elif len(sup) == len((list(shortest_sup))[0]):
            shortest_sup.add(sup)
        ###
    return shortest_sup

# print(scs(['ACGGATGAGC', 'GAGCGGA', 'GAGCGAG']))
# print(scs(['ABC', 'BCA', 'CAB']))
#print(len(scs(['CCT', 'CTT', 'TGC', 'TGG', 'GAT', 'ATT'])))
#print(scs(['CCT', 'CTT', 'TGC', 'TGG', 'GAT', 'ATT']))

# Greedy shortest common superstring (may return not the shortest sequence, but may still collapse repetitives)
def pick_maximal_overlap(reads, k):
    """ Return a pair of reads from the list with a
        maximal suffix/prefix overlap >= k.  Returns
        overlap length 0 if there are no such overlaps."""
    ### hw4(3) ###
    reada, readb = None, None
    best_olen = 0
    # for a, b in permutations(reads, 2):
    dic = {}
    for r in reads:
        kmerSet = set()
        for i in range(len(r) - k + 1):
            kmerSet.add(r[i:i + k])
        for kmer in kmerSet:
            if not kmer in dic.keys():
                dic[kmer] = set()
            dic[kmer].add(r)
    # olaps = {}  # dictionary {(r,r2):maxOverlapLen, ...}
    # try not call overlap if r doesn't contain r2's kmer suffix
    for a in reads:
        for b in dic[a[-k:]]:
            if a != b:
    ###
                olen = overlap(a, b, min_length=k)
                if olen > best_olen:
                    reada, readb = a, b
                    best_olen = olen
    return reada, readb, best_olen

def greedy_scs(reads, k):
    """ Greedy shortest-common-superstring merge.
        Repeat until no edges (overlaps of length >= k) remain. """
    read_a, read_b, olen = pick_maximal_overlap(reads, k)
    while olen > 0:
        reads.remove(read_a)
        reads.remove(read_b)
        reads.append(read_a + read_b[olen:])
        read_a, read_b, olen = pick_maximal_overlap(reads, k)
    ### hw4 ###
    # return ''.join(reads)  # join the remaining reads
    sequence = ''.join(reads)
    countA = 0
    countT = 0
    for i in range(len(sequence)):
        if sequence[i] == 'A':
            countA += 1
        elif sequence[i] == 'T':
            countT += 1
    return countA, countT
    ###


#print(greedy_scs(['ABC', 'BCA', 'CAB'], 2))  # CABCA
#print(greedy_scs(['ABCD', 'CDBC', 'BCDA'], 1))  # CDBCABCDA; As a trade off for shorter time,
# greedy method is worse in finding the shortest string than the brute force method
#print(scs(['ABCD', 'CDBC', 'BCDA']))  # ABCDBCDA

### hw4(3) ###
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
virus_sequences, _ = readFastq('ads1_week4_reads.fq')

# print(len(greedy_scs(virus_sequences, 40)))  # Total len = 15894
print(greedy_scs(virus_sequences, 40))  # A: 4633, T: 3723