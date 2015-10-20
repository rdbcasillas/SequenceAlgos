fastq = open('/Users/rdbcasillas/programming/SequenceAlgos/SRR835775_1.first1000.fastq')

def readfastq():
    sequences = []
    quals = []

    while True:
        fastq.readline()
        seq = fastq.readline().rstrip()
        fastq.readline()
        qual = fastq.readline().rstrip()
        if len(seq) == 0:
            break
        sequences.append(seq)
        quals.append(qual)

    return sequences, quals

sequences, qualities = readfastq()

print sequences[1], qualities[:5]
