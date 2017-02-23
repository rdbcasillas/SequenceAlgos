#!/usr/bin/python

#Read the fasta file and store its lines into a python list(array)
with open("./5/allReads_160505.fasta") as f:
    fasta2 = [x.strip("\n") for x in f.readlines()]

#Declare list variables to store ids and sequence from fasta
ids = []
sequences = []

#perform operations and capture ids & sequences in separate lists
for i in xrange(0,len(fasta2),7):
    id = fasta2[i].split('|')[0] + "|"
    ids.append(id)
    sequences.append('\n'.join(fasta2[i+1:i+7]))


#store content from gast file into a list
taxonomy=[]
with open("./5/allReads_160505.gast") as gast:
    for line in gast:
        line = line.split('\t')[1]
        if line != "taxonomy":
            taxonomy.append(line)

#Combine ids & taxonomy information to form defline
deflines=[]
for i, j in zip(ids, taxonomy):
    defline = i + j
    deflines.append(defline)

#Combine the defline & sequences 
annotated_list =[]
for i in xrange(0,len(deflines)):
    annotated_list.append(deflines[i])
    annotated_list.append(sequences[i])

#store the contents into a new fasta file
fasta2 = open("./5/allReads_160505_annotated.fasta", "w")
for i in annotated_list:
    fasta2.write("%s\n" % i)

