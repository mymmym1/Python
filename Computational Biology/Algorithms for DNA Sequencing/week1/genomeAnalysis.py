import matplotlib.pyplot as plt
import collections

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

sequences, qualities = readFastq('SRR835775_1.first1000.fastq')
# print(sequences[:5])
# print(qualities[:5])

def phred33ToQ(qual):
    return ord(qual) - 33
print(phred33ToQ('#'))

def createHist(qualities):
    hist = [0] * 50  # create a list with 50 elements
    for qual in qualities:  # one qualities list element qual
        for phred in qual:  # Each char qual is phred
            q = phred33ToQ(phred)
            hist[q] += 1  # increment the histogram that has value Q, notice that Q value is limited to 0-49
    return hist
h = createHist(qualities)
# print(h)
plt.bar(range(len(h)), h)
plt.show()

def findGCByPos(sequences):
    gc = [0] * 100
    totals = [0] * 100
    for seq in sequences:
        for i in range(len(seq)):
            if seq[i] == 'C' or seq[i] == 'G':
                gc[i] +=1
            totals[i] += 1
    for i in range(len(gc)):
        if totals[i] > 0:
            gc[i] /= float(totals[i])
    return gc
gc = findGCByPos(sequences)
# plt.plot(range(len(gc)), gc)
# plt.show()

count = collections.Counter()
for seq in sequences:
    count.update(seq)
# print(count)

def naive(p, t):
    occurences = []
    for i in range(len(t) - len(p) + 1):  # Loop over alignments
        match = True
        for j in range(len(p)):
            if t[i + j] != p[j]:  # can also be written: if not t[i + j] == p[j]:
                match = False  # if True, keep on this for loop, not go to the next if
                break  # break this for loop and go to the first for loop
        if match:
            occurences.append(i)  # only i: the matching index in t; Go to the next i of the outer for loop
    return occurences
t = 'AGCTTAGATAGC'
p = 'AG'
print(naive(p, t))
