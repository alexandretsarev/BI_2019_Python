### filter_2_fastq.py functions:    
1. to filter by minimal lenght  
2. to filter by GC-content (by mimial percentage of G/C nucleotides or by interval e.g. 50-70%)  
3. CROP (Trimmomatic function)  
4. HEADCROP (Trimmomatic function) 
5. TRAILING (Trimmomatic function) 
6. LEADING (Trimmomatic function) 
7. SLIDINGWINDOW (Trimmomatic function)   
8. to collect statistics after filtering in a separate file  
  (it adds "\_\__statistics.txt")  
  
   FILTER STATISTICS:  
   Total number of reads 15  
   Total valid reads 12 (80.0%)  
   Total failed reads 3 (20.0%)  
   Failed by length reads 3 (20.0%)  
   Failed by GC-content reads 0 (0.0%)  

9. to keep filtered and passed reads in separate files  
  (it adds "\_\_passed.fastq" and "\_\_failed.fastq") to the end of the files respectively   

### NB!  
it works only with phred33 quality!  

### Arguments  
```
positional arguments:  
  input                 input fastq file  

optional arguments:  
  -h, --help            show this help message and exit  
  -ml MIN_LENGTH, --min_length MIN_LENGTH  
                        filter by minimal length of the read  
  -gc , --gc_bounds     percent range of GC content (it could take 1 or 2 arguments)    
  -o ,--output_basename path to output file  
  -kf, --keep_filtered  keep filtered reads in a separate file  
  -stat,--stat_summary  keep summary statistics in file  
  -c , --CROP           cut the read to a specified length by removing bases from the end  
  -hc , --HEADCROP      cut the specified number of bases from the start of the read  
  -t , --TRAILING       cut bases off the end of a read, if below a threshold quality  
  -l , --LEADING        cut bases off the start of a read, if below a
                        threshold quality  
 
 -sw  , --SLIDINGWINDOW it takes 2 arguments quality and window size and
                        performs a sliding window trimming approach. It starts
                        scanning at the 5-prime end and clips the read once
                        the average quality within the window falls below a
                        threshold  

```
### Example usage  

```
./filter_2_fastq.py example.fastq -ml 20 -gc 12 95 -sw 20 5 -hc 5 -c 25 -kf -stat -o ./path_to_directory/processed_file  
```

### Homework  
https://www.notion.so/13th-homework-7afd23ec094e4e5b97549ab45d0c96e6  
