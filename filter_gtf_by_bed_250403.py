import pandas as pd
import sys
import csv

def extract_transcript_id(attribute_str):
    """extract transcript_id from GTF file"""
    return next((attr.split(' ')[1].replace('"', '') for attr in attribute_str.split(';') if attr.strip().startswith("transcript_id")), None)

def filter_gtf_by_bed(bed_file, gtf_file, output_file):
    try:
        # load BED file
        bed_df = pd.read_csv(bed_file, sep='\t', header=None, usecols=[3, 5, 9, 11, 12, 13],
                             names=['bed_col4', 'tStrand', 'repeatname', 'rStrand', 'class', 'subclass'])
    except FileNotFoundError:
        print(f"Error: BED file '{bed_file}' not found.")
        sys.exit(1)

    try:
        # load GTF file
        gtf_df = pd.read_csv(gtf_file, sep='\t', header=None, comment='#', names=range(9))
    except FileNotFoundError:
        print(f"Error: GTF file '{gtf_file}' not found.")
        sys.exit(1)
    
    # extract transcript_id (column[9])
    gtf_df['transcript_id'] = gtf_df[8].apply(extract_transcript_id)
    
    # Extract rows where the value in the fourth column matches `transcript_id`.
    filtered_gtf = gtf_df[gtf_df['transcript_id'].isin(bed_df['bed_col4'])]
    
    # Group BED entries by `transcript_id` and merge unique values. 
    grouped = bed_df.groupby('bed_col4').agg(lambda x: ','.join(sorted(set(x.dropna())))).reset_index()
    
    # Merge with GTF file
    annotated_gtf = filtered_gtf.merge(grouped, left_on='transcript_id', right_on='bed_col4', how='left')
    
    # Replace missing values (NaN) with empty strings.
    annotated_gtf.fillna('', inplace=True)
    
    def format_attributes(row):
        """Format the GTF attribute field and add new attributes."""
        attr = row[8].rstrip(';')  # Remove last ';'
        if row[2] == 'transcript':  
            attr += f'; class "{row["class"]}"; subclass "{row["subclass"]}"; repeatname "{row["repeatname"]}"'
            attr += f'; sense "{ "yes" if row["tStrand"] == row["rStrand"] else "no" }"'
        return attr
    
    # Add new attribute information.
    annotated_gtf[8] = annotated_gtf.apply(format_attributes, axis=1)
    
    # Remove column used for merge
    annotated_gtf.drop(columns=['transcript_id', 'bed_col4', 'tStrand', 'repeatname', 'rStrand', 'class', 'subclass'], inplace=True)
    
    # Save the result in GTF format.
    annotated_gtf.to_csv(output_file, sep='\t', index=False, header=False, quoting=csv.QUOTE_NONE)
    
    print(f"Filtered GTF file saved to {output_file}")

if __name__ == "__main__":
    # Check command-line arguments.
    if len(sys.argv) != 4:
        print("Usage: python script.py <bed_file> <gtf_file> <output_file>")
        sys.exit(1)
    
    # Get the input and output file paths.
    bed_file, gtf_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    filter_gtf_by_bed(bed_file, gtf_file, output_file)
