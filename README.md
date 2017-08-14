## SELECT_HITS
     
### Author: Shruti Srivastava

This script extracts sequences from a FASTA file 
for each interval defined in a csv file.

#### Inputs: 
1) A hits coordinate f(csv) with columns in this order:
Query_ID, Query_start, Query_end

For example - Hits_coordinates.csv

|Query|qstart|qend|
| ------------- |:-------------:| -----:|
|SEQ-A|7|24|
|SEQ-A|8|14|
|SEQ-A|21|22|
|SEQ-B|7|10|
|SEQ-B|8|14|
|SEQ-B|21|22|
|SEQ-C|21|22|
|SEQ-C|7|12|
|SEQ-D|15|84|
|SEQ-D|19|30

2) A FASTA file of protein sequences

For example - protein.fa

#### Output: A fasta file containing sequences that 
correspond to the input coordinate file
[Default: out.fa]

#### USAGE: 

python improved_select_hits.py -h [HELP]

python improved_select_hits.py -i <input_filename> -o<output_filename> -p <protein_filename>

#### For example - 
python improved_select_hits.py -i Hits_coordinates.csv -p protein.fa -o hits.fa
