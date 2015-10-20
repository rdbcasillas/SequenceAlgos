fastq = open('/Users/rdbcasillas/programming/SequenceAlgos/genomicData/SRR835775_1.first1000.fastq')
import matplotlib.pyplot as pl

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

def qualConversion(qual):
    return ord(qual) - 33

def createHistogram(quals):
    hist = [0] * 50
    for qual in quals:
        for phred in qual:
            q = qualConversion(phred)
            hist[q] += 1
    return hist

sequences, qualities = readfastq()

histogram = createHistogram(qualities)

pl.bar(range(len(histogram)), histogram)
print histogram

pl.show()
