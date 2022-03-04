import random

def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome

genome = readGenome('phix.fa')

def naive(p, t):  # p: fragment, t: genome
    matchIndices = []  # a list of the matching index in t
    ###
    charComp = 0
    numAlignTried = 0
    ###
    for i in range(len(t) - len(p) + 1):  # Loop over alignments
        ###
        numAlignTried += 1
        ###
        match = True
        for j in range(len(p)):
            ###
            charComp += 1
            ###
            if t[i + j] != p[j]:  # can also be written: if not t[i + j] == p[j]:
                match = False  # if True, keep on this for loop, not go to the next if
                break  # break this for loop and go to the first for loop
        if match:
            matchIndices.append(i)  # only i: the matching index in t; Go to the next i of the outer for loop
    ###
    return matchIndices, numAlignTried, charComp
    ###

### hw2 ###
p = 'word'
t = 'there would have been a time for such a word'
occurrences, num_alignments, num_character_comparisons = naive(p, t)
# print(occurrences, num_alignments, num_character_comparisons)

p = 'needle'
t = 'needle need noodle needle'
occurrences, num_alignments, num_character_comparisons = naive(p, t)
#print(occurrences, num_alignments, num_character_comparisons)

humanChrom1_sequences = readGenome('chr1GRCh38excerpt.fasta')

p = 'GGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGG'
occurrences, num_alignments, num_character_comparisons = naive(p, humanChrom1_sequences)
print(occurrences, num_alignments, num_character_comparisons)
###

# Generate reads from random positions in the given genome
def generateReads(genome, numReads, readLen):
    reads = []  # a list of string
    for _ in range(numReads):
        start = random.randint(0, len(genome) - readLen)  # randint includes both start and end
        reads.append(genome[start: start + readLen])
    reads = genome[start: start + readLen]
    return reads
reads = generateReads(genome, 100, 100)
'''
numMatched = 0
for r in reads:  # reads from genome must be 100% correct
    matchIndices = naive(r, genome)
    if len(matchIndices) > 0:
        numMatched += 1
# print('%d /%d reads matched exactly!' % (numMatched, len(reads)))
'''
# Machine read sequence
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

phix_sequences, _ = readFastq('ERR266411_1.first1000.fastq')  # We are not interested in qualities, so use _
'''
# Compare machine read sequence fragments (100 bases each) with reference genome
numMatched = 0
len_phix_sequences = 0  # length of the string list
for r in phix_sequences:  # each string in the string list
    len_phix_sequences += 1
    matchIndices = naive(r, genome)
    if len(matchIndices) > 0:  # even if there are multiple indices match this sequence in the genome
        numMatched += 1  # means this reading line has matches
# print('%d /%d reads matched exactly!' % (numMatched, len_phix_sequences))  # => 7/1000, sequencing error is profound
'''
'''
# Try reducing to compare 30-base fragment - prefix match
numMatched = 0
len_phix_sequences = 0  # length of the string list
for r in phix_sequences:  # each string in the string list
    len_phix_sequences += 1
    r = r[:30]
    matchIndices = naive(r, genome)
    if len(matchIndices) > 0:  # even if there are multiple indices match this sequence in the genome
        numMatched += 1  # means this reading line has matches
# print('%d /%d reads matched exactly!' % (numMatched, len_phix_sequences))  # => 459/1000, still not very high,
# because read could come from the complement strand of DNA
'''
def reverseComplement(sequence):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    RevSequence = ''
    for base in sequence:  # read string from left to write
        RevSequence = complement[base] + RevSequence  # add base from right to left
    return RevSequence

# Try adding complement genome for fragment comparison
numMatched = 0
len_phix_sequences = 0  # length of the string list
for r in phix_sequences:  # each string in the string list
    len_phix_sequences += 1
    r = r[:30]
    matchIndices = naive(r, genome)
    # matchIndices.extend(naive(r, reverseComplement(genome)))  # will yield the same result
    matchIndices.extend(naive(reverseComplement(r), genome))  # Will include the matchIndices appeared before,
    # but as long as len(matchIndices) > 0 will numMatched += 1
    if len(matchIndices) > 0:  # even if there are multiple indices match this sequence in the genome
        numMatched += 1  # means this reading line has matches
# print('%d /%d reads matched exactly!' % (numMatched, len_phix_sequences)) # => 932/1000
