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

def reverseComplement(string):
    dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
    reverse = ''
    for i in string:
        reverse = dict[i] + reverse
    return reverse

def patternMatchStrandAware(p, sequence):
    occurrences = []
    rev_p = reverseComplement(p)
    for i in range(len(sequence) - len(p) + 1):
        Match = True
        flag = True 
        flag2 = True
        for j in range(len(p)):
            if flag:
                if sequence[i+j] != p[j]: 
                    flag = False    
            if flag2:
                if sequence[i+j] != rev_p[j] :
                    flag2 = False
            if not (flag or flag2):
                Match = False
                break
        if Match:
            occurrences.append(i)
    return  occurrences

def approxPatternMatcher(p, sequence):
    occurrences = []
    for i in range(len(sequence) - len(p) + 1):
        count = 0
        Match = True
        for j in range(len(p)):
            if sequence[i+j] != p[j]:
                    count += 1
            if count > 2 : 
                Match = False
                break
         
        if Match:
            occurrences.append(i)
    return occurrences
refGenome = open('/Users/rdbcasillas/programming/SequenceAlgos/genomicData/lambda_virus.fa')
genome = getGenome(refGenome)
print (patternMatchStrandAware('AGTCGA',genome))
print (approxPatternMatcher('AGGAGGTT', genome))
