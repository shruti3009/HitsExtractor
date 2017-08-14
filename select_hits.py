#!/usr/bin/env python
"""
SELECT_HITS
Author: Shruti Srivastava

This script extracts sequences from a FASTA file 
for each interval defined in a csv file.

Inputs: 
1) A hits coordinate f(csv) with columns in this order:
Query_ID, Query_start, Query_end

2) A FASTA file of protein sequences

Output: A fasta file containing sequences that 
correspond to the input coordinate file
[Default: out.fa]
"""

from Bio import SeqIO
import sys,getopt,time
        
__title__ = 'Select_Hits'
__version__ = 'v2.0'
__description__ = "A tools to fetch sequences based on a coordinate file"
__author__ = 'Shruti Srivastava'
__comment__ = 'A part of my Mimic pipeline'
__author_email__ = "shruti.srivastava@ucalgary.ca"
epi = "By %s. %s <%s>\n\n" % (__author__,
__comment__,
__author_email__)
__doc__ = "\n***********************************************\
************************************\
\n %s v%s - %s \n**********************************\
***********************************************\
**\n%s" % (__title__,
__version__,
__description__,
epi)


def file_to_dict(protname):
   '''
    Makes a record dictionary with sequence ids as keys
    and sequences as values.
    (str) -> (dict)
    
    Input: Protein file name
    
    Returns: a dictionary of fasta records
   '''     

   #Create a new dictionary named rec_dict 
   rec_dict = {}
   
   #Use standard Sequence Input/Output interface for BioPython to read the fasta file
   record_iterator = SeqIO.parse(protname, "fasta")

   #Read record one by one and store it in rec_dict with key as record.id
   #(i.e. fasta header) and value as record.seq (i.e. fasta sequence)
   for record in record_iterator:
       rec_dict[str(record.id)] = str(record.seq) 

   return(rec_dict)



def extract_write_seqs(rec_dict, fname, output_filename):
    
     '''
     This functions writes the sequences corresponding 
     to the coordinate file in the output file.
     (dict, str, str) -> int
     
     Inputs: Record dictionary, coordinate filename,
             output filename
     
     Returns: 1, if runs successfully
     '''
     
     #Open the coordinates file with a file handler in read mode
     fhandler = open(fname, 'r')
     
     #Open the output file in write mode with file handler 'out'
     out = open(output_filename, 'w')


     #Read through the coordinate file     
     for line in fhandler:
     
     #Skip the line if it starts with the word Query
        if line.startswith("Query"):
            continue
    
        #removes whitespace at the end of the line
        line.rstrip()
    
        #Split the line by commas and store it in the form of a list in lst
        lst = line.split(',')
    
        #Assign variable 'header' to the first item in that list
        header = lst[0]
    
        #Assign varibale 'start' to the second item in the list
        start = int(lst[1])
    
        #Assign variable 'end' to the third item in the list
        end = int(lst[2])
   
        #if the the header from the coord file is present in rec_dict,ie, 
        if str(header) in rec_dict: 
            '''      
            Substring the original sequences as per the coordinates and write in 
            the output file in FASTA format. The new header will look like
            >OldHeader_StartCoordinate_EndCoordinate 
            '''
            out.write('>' + str(header) + '_' + str(start) + '_' + str(end) + "\n" + (rec_dict[str(header)][start-1:end]) + "\n")
        
     return 1 

def usage():
    print("Usage: python improved_select_hits.py -i <input_filename> -o\
<output_filename [Default: out.fa]> -p <protein_filename>\n")
    sys.exit(2) #Exit the program


def main(argv):
    
   #Checking if no input has been provided 
   if(len(argv)==0):
        print('\nERROR!:No input provided\n')
        usage()
        
   #Default output filename
   output_filename = 'out.fa'
   
   #Try and Catch block for handling input errors
   try:
      opts, args = getopt.getopt(argv,"h:i:o:p:",["help=","ifile=","ofile=","pfile="])
      
   except getopt.GetoptError:
      print(__doc__)
      usage()
     
   #Check whether the mandatory files are given as inputs  
   short_opts = [i[0] for i in opts]
   if(('-p') not in short_opts) or (('-i') not in short_opts):
       print ("ERROR: Missing inputs. Please provide -i and -p")
       usage()

   #Reading user inputs
   for opt, arg in opts:
       
      if opt == '-h':
         print(__doc__)
         usage()
         sys.exit()

      elif opt in ("-i", "--ifile"):
         fname = arg

      elif opt in ("-o", "--ofile"):
         output_filename = arg
         
      elif opt in ("-p", "--pfile"):
         protname = arg               
 
   print(__doc__,'Input file is %s\n Output file is %s' %( protname, output_filename))
   print( '----------------------------------------\nRunning Script\n--------------\
--------------------------\n')
   
   #Variable to record time 
   start_time = time.time()
 
   #Calling function and storing the returned dicts 
   rec_dict = file_to_dict(protname)
   
   #Calling function and storing the returned value
   success = extract_write_seqs(rec_dict, fname, output_filename)
   
   #Checking if everything ran successfully
   if(success):
       print ('Done! Time elapsed: %.4f seconds' % (time.time() - start_time))


if __name__ == "__main__":
    
   #Call main function with the input arguments 
   main(sys.argv[1:])
