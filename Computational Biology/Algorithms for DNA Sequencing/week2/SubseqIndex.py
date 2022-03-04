import bisect

class SubseqIndex(object):
    """ Holds a subsequence index for a text T """

    def __init__(self, t, k, ival):
        """ Create index from all {t-subseqs consisting of k characters
            spaced ival positions apart}.  E.g., SubseqIndex("ATAT", 2, 2)
            extracts ("AA", 0) and ("TT", 1) at in index 0 and index 1"""
        self.k = k  # num characters per subsequence extracted
        self.ival = ival  # space between them; 1=adjacent, 2=every other, etc
        self.index = []
        self.span = 1 + ival * (k - 1)
        for i in range(len(t) - self.span + 1):  # for each subseq
            self.index.append((t[i:i + self.span:ival], i))  # add (subseq, index of in which turn find subseq)
            #e.g. t[1:1+3:2]=t[1:4:2], add from index=1, not include index=4, 2 means every other.
        self.index.sort()  # alphabetize by subseq

    def query(self, p):
        """ Return index hits for first p-subseq """
        subseq = p[:self.span:self.ival]  # query with first subseq
        ### hw2, NO6 ###
        l = len(subseq)
        ###
        i = bisect.bisect_left(self.index, (subseq, -1))  # binary search find the first position p-subseq occurs in t-index list, i!=index's offset
        hits = []
        while i < len(self.index):
            ### hw2, NO6 ###
            if self.index[i][0][:l] != subseq:
            ###
                break
            hits.append(self.index[i][1])
            i += 1
        return hits  # Just t-index hit, doesn't necessarily mean p match

ind = SubseqIndex('ATATAT', 3, 2)
# print(ind.index)  # [('AAA', 0), ('TTT', 1)]
p = 'TTATAT'
# print(ind.query(p[0:]))  # []
# print(ind.query(p[1:]))  # [1]

### hw2, NO6: Subsequence-assisted index hit ###
def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome
humanChrom1_sequences = readGenome('chr1GRCh38excerpt.fasta')

p = 'GGCGCGGTGGCTCACGCCTGTAAT'
subseqIndex = SubseqIndex(humanChrom1_sequences, 8, 3)

def approximate_match_subseqIndex(p, t, n):  # n is the max allowed edits
    segment_length = int(round(len(p) / (n+1)))
    index_hit = 0
    for i in range(n+1):
        start = i*segment_length
        end = min((i+1)*segment_length, len(p))  # 1 more than the end index
        num_hit = len(subseqIndex.query(p[start:end]))
        index_hit += num_hit
    return index_hit

matchSubseqInd = approximate_match_subseqIndex(p, humanChrom1_sequences, 2)
print("total index hits are: %d" % matchSubseqInd)





