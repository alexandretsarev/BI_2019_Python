### filter_2_fastq.py functions:    
1. to filter by minimal lenght  
2. to filter by GC-content (by mimial percentage of G/C nucleotides or by interval e.g. 50-70%)  
3. crop (Trimmomatic function)  
4. headcrop (Trimmomatic function) 
5. trailing (Trimmomatic function) 
6. leading (Trimmomatic function) 
7. slidingwindow (Trimmomatic function)   
8. to collect statistics after filtering in a separate file  
  ("*\_\__statistics.txt")  
  
   FILTER STATISTICS:  
   Total number of reads 15  
   Total valid reads 12 (80.0%)  
   Total failed reads 3 (20.0%)  
   Failed by length reads 3 (20.0%)  
   Failed by GC-content reads 0 (0.0%)  

9. to keep filtered and passed reads in separate files  
  ("*\_\_passed.fastq" and "*\_\_failed.fastq")  

### NB!  
it works only with phred33 quality!  

### Arguments  
```
positional arguments:
  input                input fastq file

optional arguments:
  -h, --help           show this help message and exit  
  --min_length         minimal length  
  --gc_bounds  [ ...]  percent range of GC content   
  --output_basename    path to output file  
  --keep_filtered      keep filtered reads in a separate file  
  --stat_summary       keep summary statistics in file  
  --crop               cut the read to a specified length by removing bases from the end  
  --headcrop           cut the specified number of bases from the start of the read  
  --trailing           cut bases off the end of a read, if below a threshold quality   
  --leading            cut bases off the start of a read, if below a threshold quality  
  --slidingwindow      it takes 2 arguments quality and window size and performs a sliding 
                       window trimming approach; it starts scanning at the 5'-end and clips 
                       the read once the average quality within the window falls below a threshold  



```
### Example usage  

```
./filter_2_fastq.py example.fastq --min_length 20 --gc_bounds 12 95 --slidingwindow 20 5 --headcrop 5 --crop 25 --keep_filtered --stat_summary  --output_basename path_to_directory/processed_file 
```

### Homework source
https://www.notion.so/13th-homework-7afd23ec094e4e5b97549ab45d0c96e6  
