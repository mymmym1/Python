import bisect
# find the matched first p-kmer indices in kmer processed t
class IndexKmer(object):
    def __init__(self, t, k):  # t: genome text. k: k-mer length
        self.k = k
        self.index = []  # (k-mer, offset) pair list, offset is the index of in which turn find subseq
        for i in range(len(t) - k + 1):  # for each kmer in t
            self.index.append((t[i:i + k], i))  # preprocess t with kmers
        self.index.sort()  # alphabetize by kmers in t

    def query(self, p):
        ''' Return index hits for first kmer of P '''
        kmer = p[:self.k]  # query with first kmer in p
        i = bisect.bisect_left(self.index, (kmer, -1))  # binary search find the first position p-kmer occurs in t-index list, i!=index's offset
        # index is a list of tuple (k-mer, offset). Since all the indices of kmer > -1, we will get the first index.
        hits = []  # list of t-kmer indices
        # The following collect matching index entries
        while i < len(self.index):  # i is the first p-kmer occurrance in t, self.index belong to t-kmer lists
            if self.index[i][0] != kmer:  # if the tuple(t-kmer, offset)'s t-kmer != first p-kmer,
                break  # e.g. this will occur after several i += 1, when the next t-kmer != first p-kmer (all the alphabetic ordered first p-kmer has been searched up)
            hits.append(self.index[i][1])  # append this t-kmer offsets
            i += 1
        return hits

# Check the rest beyond p-kmer, find the matched fragment p's t indices
def queryPIndex(p, t, indexKmer):  # p: fragment (contains first p-kmer)
    k = indexKmer.k  # k-mer length (k)
    offsets = []  # offsets of the matched p
    ### 5 ###
    num_hit = 0
    ### 5 ###
    for i in indexKmer.query(p):  # i: every index with a matched first p-kmer
        ### 5 ###
        num_hit += 1
        ### 5 ###
        if p[k:] == t[i+k:i+len(p)]:  # verify that rest of P matches
            offsets.append(i)
    return offsets, num_hit

t = 'GCTACGATCTAGAATCTA'
p = 'TCTA'
indexKmer = IndexKmer(t, 2)
# print(queryPIndex(p, t, indexKmer))

### hw2: Index-assisted approximate matching ###
# Implement the pigeonhole principle using IndexKmer to find exact matches
def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome
humanChrom1_sequences = readGenome('chr1GRCh38excerpt.fasta')

indexKmer = IndexKmer(humanChrom1_sequences, 8)
def approximate_match_index(p, t, n):  # n is the max allowed edits
    segment_length = int(round(len(p) / (n+1)))
    all_matches = set()  # no repetition in set()
    ### 5 ###
    index_hit = 0
    ### 5 ###
    for i in range(n+1):
        start = i*segment_length
        end = min((i+1)*segment_length, len(p))  # 1 more than the end index
        ### 5 ###
        _, num_hit = queryPIndex(p[start:end], t, indexKmer)
        index_hit += num_hit
        offsets, _ = queryPIndex(p[start:end], t, indexKmer)  # check the occurrence t indices of each fragment
        ### 5 ###
        # Extend matching segments to see if whole p matches
        for m in offsets:
            if m < start or m-start+len(p) > len(t):  # Which index shouldn't happen, if compare full p to t,
                continue  # so ignore such match, and continue to see next m in this for loop
            mismatches = 0
            for j in range(0, start):  # Check the previous part before p[start:end]
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    if mismatches > n:
                        break  # break this for loop, but still need to check the following statements, before doing the next m in the outer for loop
            for j in range(end, len(p)):  # Check the post part after p[start:end]
                if not p[j] == t[m-start+j]:
                    mismatches += 1
                    if mismatches > n:
                        break
            if mismatches <= n:  # if mismatch # is less than max allowed, assume it is a match
                all_matches.add(m - start)  # indices on t, won't repeatedly add the same index
    ### 5 ###
    print("total index hits are: %d" % index_hit)
    ### 5 ###
    return list(all_matches)

p = 'GGCGCGGTGGCTCACGCCTGTAAT'
print(len(approximate_match_index(p, humanChrom1_sequences, 2)))  # up to 2 mismatches

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
# print(len(naive_2mm(p, humanChrom1_sequences)))
# Also gives 19 matches, but calculation speed may be slower than skipping algorithms