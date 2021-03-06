fastq = open('/Users/rdbcasillas/programming/SequenceAlgos/genomicData/ERR037900_1.first1000.fastq')
import matplotlib.pyplot as pl
import itertools

#Read the fastq to get all sequences and corresponding qualities in separate lists  
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

#convert the quality into phred score
def qualConversion(qual):
    return ord(qual) - 33

#Find the total qualities for a particular sequence cycle
def seqcycleQC(sequences, quals):
    dictionary = {}
    for seq,qual in zip(sequences,quals):
        for i in range(len(seq)):
            if i in dictionary: 
                dictionary[i] += qualConversion(qual[i]) 
            else:
                dictionary[i] = qualConversion(qual[i])
    return dictionary


#Create a histogram that lists the count of a quality score
def createHistogram(quals):
    hist = [0] * 50
    for qual in quals:
        for phred in qual:
            q = qualConversion(phred)
            hist[q] += 1
    return hist

sequences, qualities = readfastq()

histogram = createHistogram(qualities)

print seqcycleQC(sequences,qualities)
#pl.bar(range(len(histogram)), histogram)
#print histogram

#pl.show()
