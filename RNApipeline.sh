#!/bin/bash

################################################################################
###### A script that automates the RNAseq pipeline##############################
###### variables need to be manually changed depending on system#################
###### RNA-seq Tools are assumed to have been installed globally#################
#################################################################################   


#exit the script if errors
set -e
set -u
set -o pipefail 

#set up variables
PROJDIR="/home/vats/classProj"
refTranscript="${PROJDIR}/ref-transcripts.gtf"
sampleName=$2
P=8
INDEX="/usr/local/share/bcbio/genomes/Hsapiens/GRCh37/bowtie2/GRCh37"
REFERENCE="/usr/local/share/bcbio/genomes/Hsapiens/GRCh37/seq/GRCh37.fa"

mkdir ${PROJDIR}/${sampleName}RNA ${PROJDIR}/${sampleName}Assembly ${PROJDIR}/${sampleName}_cuffdiff

fastq-dump.2 -O $PROJDIR/${sampleName}RNA $1

tophat -o $PROJDIR/${sampleName}RNA -p $P -G $refTranscript $INDEX $PROJDIR/${sampleName}RNA/${1}.fastq

cufflinks -q -p $P -o $PROJDIR/${sampleName}Assembly -g $refTranscript $PROJDIR/${sampleName}RNA/accepted_hits.bam 

cp $PROJDIR/pancreasAssembly/GTFs.txt $PROJDIR/${sampleName}Assembly/

sed "s/pancreasAssembly/${sampleName}Assembly/" $PROJDIR/${sampleName}Assembly/GTFs.txt

cuffmerge -s $REFERENCE -g $refTranscript -p $P -o $PROJDIR/${sampleName}Assembly/merged $PROJDIR/${sampleName}Assembly/GTFs.txt 

cuffdiff -p $P -o $PROJDIR/${sampleName}_cuffdiff $refTranscript $PROJDIR/controlRNA/accepted_hits.bam $PROJDIR/${sampleName}RNA/accepted_hits.bam
