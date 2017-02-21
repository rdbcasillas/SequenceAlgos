echo -e "genome_name \t number_of_contigs \t assembly_size"
for f in 4/*
do 
    size=$(grep ">" $f | awk '{print $2}' | sed 's/^.*=//g' | awk '{s+=$1} END {print s}')
    contigs=$(grep ">" $f | wc -l)
    
    name=$(echo $f | sed 's/.contigs.fasta//g' | sed 's/4\///g')
    echo -e $name "\t" $contigs "\t" $size    
done
