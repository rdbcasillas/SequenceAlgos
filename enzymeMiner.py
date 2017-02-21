#!/usr/local/bin/python
import Bio
from Bio import SeqIO
from Bio import Seq
from Bio import SeqRecord


#function that converts fasta files into dictionaries with Seq ids as keys 
#and Seq Object as values

def fasta_as_dict():
    arabi_dict = {}
    PF00891_dict = {}
    for seq_record in SeqIO.parse("./Arabidopsis-thaliana_rna.fna","fasta"):
        arabi_dict[seq_record.id] = seq_record.seq
        
    for seq_record in SeqIO.parse("./PF00891_full_length_sequences.fasta", "fasta"):
        PF00891_dict[seq_record.id] = seq_record.seq
    
    return arabi_dict, PF00891_dict

        
#Function that collects PF00891 sequences in an array
def sequenceCollector(dictionary):
    protein_array = [str(dictionary[key]) for key in dictionary.iterkeys()]
    return protein_array
    


    
#Function that converts the raw mRNA sequences into possible amino acids 
#and stores them in a dictionary with ids as keys and an array of 
#possible proteins as values
#Only collects proteins greater than length 50. Arbitrary value since all proteins
#in PF00891 are much larger in length

def ORF_translator(sequence_dictionary):
    allORF_dict = {}
    for key in sequence_dictionary.iterkeys():
        allORF_dict[key] = []
        sequence = sequence_dictionary[key]
        for frame in range(3):
            for protein in sequence[frame:].translate().split("*"):
                if len(protein) >= 50:
                    allORF_dict[key].append(protein)
    return allORF_dict                    
                        
                        
                        
#Function that checks and collect the enzymes in a dictionary
#from Aribodopsis that are in class PF00891

def relevant_enzymes(protein_arr, allORF):
    enz_collection = {}
    for key in allORF.iterkeys():
        
        for aminoseq in allORF[key]:
            if str(aminoseq) in protein_arr:
                enz_collection[key] = []
                enz_collection[key].append(aminoseq)
    return enz_collection
                

#Function that creates a collection that stores the sorted ids since this collection 
#will be looped when creating SeqRecord objects
def sort_ids():
    ids = [key[3:] for key in unsorted_dict]
    sorted_numbers = sorted(ids)
    sorted_ids = ['NM_'+ num for num in sorted_numbers]
    return sorted_ids


#store arabidopsis and PF00891 fasta files as a dictionaries       
dict_arabi, dict_PF00891 = fasta_as_dict()

#convert arabidopsis sequences into possible protein coding sequences
dict_allORF = ORF_translator(dict_arabi)

#store PF00891 sequences in an array
PF00891_sequences = sequenceCollector(dict_PF00891)

#store arabidopsis sequences which are in class PF00891 
unsorted_dict= relevant_enzymes(PF00891_sequences, dict_allORF)

#store sorted ids
sorted_ids = sort_ids()


#Create a fasta file to store the amino acid sequences along with ids
with open("Arabi_methyltranferase.fasta", "w") as test_file:
    for accession in sorted_ids:
        test_file.write(">" + accession + "|" + "len: " + str(len(unsorted_dict[accession][0])) + "\n")
        test_file.write(str(unsorted_dict[accession][0]) + "*" + "\n" + "\n")



#SeqIO can take SeqRecords and directly create fasta files but there won't be any line breaks! 
#enzyme_sequences = []
#for accession in sorted_ids:
#    record = SeqRecord.SeqRecord(id=accession,description="len: "+ str(len(unsorted_dict[accession][0])), seq=unsorted_dict[accession][0])
#    enzyme_sequences.append(record)   
#SeqIO.write(enzyme_sequences, "my_example.fasta", "fasta")
