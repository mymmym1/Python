# Avoid overcolapsing (may cause shuffling around between repetivies)
def de_bruijn_ize(st, k):
    """ Return a list holding, for each k-mer, its left
        k-1-mer and its right k-1-mer in a pair """
    edges = []
    nodes = set()
    for i in range(len(st) - k + 1):  # separate a string into kmers
        edges.append((st[i:i+k-1], st[i+1:i+k]))  # separate each kmer into left k-1mer and right k-1mer
        nodes.add(st[i:i+k-1])
        nodes.add(st[i+1:i+k])
    return nodes, edges

nodes, edges = de_bruijn_ize("ACGCGTCG", 3)  # The smaller k is, the more chance impacted by repeats - multiple different Eulerian walks (problems, errors).
# print(nodes)
# print(edges)

