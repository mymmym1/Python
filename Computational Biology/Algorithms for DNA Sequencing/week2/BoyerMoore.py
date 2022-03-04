def z_array(s):
    """ Use Z algorithm (Gusfield theorem 1.4.1) to preprocess s """
    assert len(s) > 1
    z = [len(s)] + [0] * (len(s) - 1)
    # Initial comparison of s[1:] with prefix
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            z[1] += 1
        else:
            break
    r, l = 0, 0
    if z[1] > 0:
        r, l = z[1], 1
    for k in range(2, len(s)):
        assert z[k] == 0
        if k > r:
            # Case 1
            for i in range(k, len(s)):
                if s[i] == s[i - k]:
                    z[k] += 1
                else:
                    break
            r, l = k + z[k] - 1, k
        else:
            # Case 2
            # Calculate length of beta
            nbeta = r - k + 1
            zkp = z[k - l]
            if nbeta > zkp:
                # Case 2a: Zkp wins
                z[k] = zkp
            else:
                # Case 2b: Compare characters just past r
                nmatch = 0
                for i in range(r + 1, len(s)):
                    if s[i] == s[i - k]:
                        nmatch += 1
                    else:
                        break
                l, r = k, r + nmatch
                z[k] = r - k + 1
    return z


def n_array(s):
    """ Compile the N array (Gusfield theorem 2.2.2) from the Z array """
    return z_array(s[::-1])[::-1]


def big_l_prime_array(p, n):
    """ Compile L' array (Gusfield theorem 2.2.2) using p and N array.
        L'[i] = largest index j less than n such that N[j] = |P[i:]| """
    lp = [0] * len(p)
    for j in range(len(p) - 1):
        i = len(p) - n[j]
        if i < len(p):
            lp[i] = j + 1
    return lp


def big_l_array(p, lp):
    """ Compile L array (Gusfield theorem 2.2.2) using p and L' array.
        L[i] = largest index j less than n such that N[j] >= |P[i:]| """
    l = [0] * len(p)
    l[1] = lp[1]
    for i in range(2, len(p)):
        l[i] = max(l[i - 1], lp[i])
    return l


def small_l_prime_array(n):
    """ Compile lp' array (Gusfield theorem 2.2.4) using N array. """
    small_lp = [0] * len(n)
    for i in range(len(n)):
        if n[i] == i + 1:  # prefix matching a suffix
            small_lp[len(n) - i - 1] = i + 1
    for i in range(len(n) - 2, -1, -1):  # "smear" them out to the left
        if small_lp[i] == 0:
            small_lp[i] = small_lp[i + 1]
    return small_lp


def good_suffix_table(p):  # p is the fragment
    """ Return tables needed to apply good suffix rule. """
    n = n_array(p)
    lp = big_l_prime_array(p, n)
    return lp, big_l_array(p, lp), small_l_prime_array(n)


def good_suffix_mismatch(i, big_l_prime, small_l_prime):
    """ Given a mismatch at offset i, and given L/L' and l' arrays,
        return amount to shift as determined by good suffix rule. """
    length = len(big_l_prime)
    assert i < length
    if i == length - 1:
        return 0
    i += 1  # i points to leftmost matching position of P
    if big_l_prime[i] > 0:
        return length - big_l_prime[i]
    return length - small_l_prime[i]


def good_suffix_match(small_l_prime):
    """ Given a full match of P to T, return amount to shift as
        determined by good suffix rule. """
    return len(small_l_prime) - small_l_prime[1]


def dense_bad_char_tab(p, amap):  # p is the fragment
    """ Given pattern string and list with ordered alphabet characters, create
        and return a dense bad character table.  Table is indexed by offset
        then by character. """
    tab = []
    nxt = [0] * len(amap)
    for i in range(0, len(p)):
        c = p[i]
        assert c in amap
        tab.append(nxt[:])
        nxt[amap[c]] = i + 1
    return tab


class BoyerMoore(object):
    """ Encapsulates pattern and associated Boyer-Moore preprocessing. """

    def __init__(self, p, alphabet='ACGT'):  # p is the fragment
        self.p = p
        self.alphabet = alphabet
        # Create map from alphabet characters to integers
        self.amap = {}
        for i in range(len(self.alphabet)):
            self.amap[self.alphabet[i]] = i
        # Make bad character rule table
        self.bad_char = dense_bad_char_tab(p, self.amap)
        # Create good suffix rule table
        _, self.big_l, self.small_l_prime = good_suffix_table(p)

    def bad_character_rule(self, i, c):  # offset i and c(mismatched base) need to be determined by yourself
        """ Return # shifts given by bad character rule at offset i """
        assert c in self.amap
        ci = self.amap[c]
        assert i > (self.bad_char[i][ci] - 1)
        return i - (self.bad_char[i][ci] - 1)

    def good_suffix_rule(self, i):  # The mismatch index i needs to be determined by yourself
        """ Given a mismatch at offset i, return amount to shift
            as determined by (weak) good suffix rule. """
        length = len(self.big_l)
        assert i < length
        if i == length - 1:
            return 0
        i += 1  # i points to leftmost matching position of P
        if self.big_l[i] > 0:
            return length - self.big_l[i]
        return length - self.small_l_prime[i]

    def match_skip(self):
        """ Return amount to shift in case where P matches T """
        return len(self.small_l_prime) - self.small_l_prime[1]

# GCTAGCTC (just imagine, not used)
# TCAA
p = 'TCAA'
p_bm = BoyerMoore(p)
numshift1 = p_bm.bad_character_rule(2, 'T')  # We see that at offset[2] on genome there is a mismatch to i[2] = 'T'
# print("Shifts given by bad character rule: %d" % numshift1)  # 2

# GCTAGCTC (just imagine, not used)
# ACTA
p = 'ACTA'
p_bm = BoyerMoore(p)
numshift2 = p_bm.good_suffix_rule(0)
# At index[0] a mismatch causes the prefix of the fragment-'A' to match the suffix of Genome suffix "CTA". This is a
# special case. If changed to ACTG, will shift 4
# print("Shifts given by good suffix rule: %d" % numshift2)  # 3

# ACACGCTC (just imagine, not used)
# ACAC
p = 'ACAC'
p_bm = BoyerMoore(p)
# print("Shifts when P matches T: %d" % p_bm.match_skip())  # 2
# This is a special case where the 1st AC in fragment will match the 2nd AC in genome
# If change to ACTG, will shift 4

def boyer_moore(p, p_bm, t):
    """ Do Boyer-Moore matching """
    i = 0
    occurrences = []
    ###
    charComp = 0
    numAlignTried = 0
    ###
    while i < len(t) - len(p) + 1:  # move fragment along genome from left to right
        ###
        numAlignTried += 1
        ###
        shift = 1
        mismatched = False
        for j in range(len(p)-1, -1, -1):  # not include index[-1], compare char on fragment from right to left
            ###
            charComp += 1
            ###
            if p[j] != t[i+j]:
                skip_bc = p_bm.bad_character_rule(j, t[i+j])  # min could be skip = 0, shift = 1
                skip_gs = p_bm.good_suffix_rule(j)  # min could be skip = 0, shift = 1
                shift = max(shift, skip_bc, skip_gs)  # at least shift = 1, select the max shift
                mismatched = True
                break
        if not mismatched:
            occurrences.append(i)
            skip_gs = p_bm.match_skip()  # shift amount
            shift = max(shift, skip_gs)
        i += shift
    ###
    return occurrences, numAlignTried, charComp
    ###

t = 'GCTAGCTCTACGAGTCTA'
p = 'TCTA'
p_bm = BoyerMoore(p, alphabet='ACGT')
# print(boyer_moore(p, p_bm, t))
# print(t[6:10])
# print(t[14:19])

### hw2 ###
p = 'word'
t = 'there would have been a time for such a word'
lowercase_alphabet = 'abcdefghijklmnopqrstuvwxyz '
p_bm = BoyerMoore(p, lowercase_alphabet)
occurrences, num_alignments, num_character_comparisons = boyer_moore(p, p_bm, t)
# print(occurrences, num_alignments, num_character_comparisons)

p = 'needle'
t = 'needle need noodle needle'
p_bm = BoyerMoore(p, lowercase_alphabet)
occurrences, num_alignments, num_character_comparisons = boyer_moore(p, p_bm, t)
# print(occurrences, num_alignments, num_character_comparisons)

def readGenome(filename):
    genome = ''
    with open(filename, 'r') as f:
        for line in f:
            if not line[0] == '>':
                genome += line.rstrip()  # remove trailing white space from the ends
    return genome

humanChrom1_sequences = readGenome('chr1GRCh38excerpt.fasta')

p = 'GGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGG'
p_bm = BoyerMoore(p, alphabet='ACGT')
occurrences, num_alignments, num_character_comparisons = boyer_moore(p, p_bm, humanChrom1_sequences)
print(occurrences, num_alignments, num_character_comparisons)
###