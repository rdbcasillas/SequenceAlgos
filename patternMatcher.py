def getGenome(fasta):
    genome = ''
    for f in fasta:
        if not f[0] == '>':
            genome = genome + f.rstrip() 
    return genome


def patternMatch(p, sequence):
    occurrences = []
    for i in range(len(sequence) - len(p) + 1):
        Match = True
        for j in range(len(p)):
            if sequence[i+j] != p[j]:
                Match = False
                break
        if Match:
            occurrences.append(i)
    return occurrences

refGenome = open('/Users/rdbcasillas/programming/SequenceAlgos/genomicData/927.fasta')
genome = getGenome(refGenome)
print patternMatch('tgaagg',genome)
