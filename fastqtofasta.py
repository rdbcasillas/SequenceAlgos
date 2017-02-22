#import regular expression package
import re

#open the fastq file and store its lines in an array
with open("./3/lbc28_AB.fastq") as f:
    content = [x.strip("\n") for x in f.readlines()]

#extract information from content variable into multiple variables after performing
#relevant operations on them. Finally store those variables inside another array.
fasta_list = []
for i in xrange(0,len(content),4):
    defline = ">" + re.sub(" ", "|", content[i])
    sequence = content[i+1]
    
    fasta_list.append(re.sub("/","|",defline))
    fasta_list.append(sequence)

#write the contents of the final array into an output fasta file    
fasta = open("./3/lbc28_AB.fasta", "w")
for i in fasta_list:
    fasta.write("%s\n" % i)

