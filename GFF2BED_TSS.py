#%%
import sys, re

#%%
argvs = sys.argv
infile = str(argvs) ## input GTF file
outfile = str(argvs[2]) ## output of TSS bed file

with open(infile, 'r') as fr, open(outfile, 'w') as fw:
    for line in fr:  # Read each line from the GFF file
        line = line.strip() # Substitute lines as a character
        
        if line.startswith('#'):  # Skip comment lines beginning with "#"
            continue
            
        else:
            match = re.search(r'transcript_id\s+"([^"]+)"', line)  # Search for the pattern transcript_id "XXXXX"
            if match:  # # If the line contains a pattern of "XXXXX",
                transcript_id = match.group(1)  # extract "XXXXX" and store it in `transcript_id`
                
                columns = line.split('\t')  # Split the line by tabs and store the resulting list in `columns`.
                
                if columns[2] == 'transcript':  # If columns[2] begin with "transcript"
                
                    if columns[6] == '+':  # Calculate the coordinate using the transcript 5' end as (columns[3]) for plus strand
                        # Output as bed file
                        fw.write(f'{columns[0]}\t{int(columns[3])-1}\t{int(columns[3])}\t{transcript_id}\t0\t{columns[6]}\n')
                        
                    elif columns[6] == '-':  # Calculate the coordinate using the transcript 5' end as (columns[6]) for minus strand
                        # Output as bed file
                        fw.write(f'{columns[0]}\t{int(columns[4])-1}\t{int(columns[4])}\t{transcript_id}\t0\t{columns[6]}\n')
# %%
