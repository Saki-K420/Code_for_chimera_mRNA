Code_for_chimera_mRNA
========================
## Overview
  `Code_for_chimera_mRNA` is a pipeline to detect "chimeric mRNAs", which are derived from Transposable element (TE). Methods for detecting chimeric mRNAs are not yet standardized. This repository include sequence of custom Python scripts for identifying potential chimeric mRNAs. 
  The workflow can be broadly divided into two categories:
### TEs as Promoters
### Downstream Genes Associated with Transposable Elements
   In this pipeline, transcription start sites (TSSs) are defined as the first nucleotide of each mRNA transcript. 
   
## Description
  ### TEs as Promoters 
    TSS of each transcript was extracted from GTF file and converted to BED file with *`GFF2BED_TSS.py`* then TSSs that overlapped with TEs were extracted. After that, generated BED file are compared with BED file of TEs (like RepeatMasker) and TSSs which overlap with TEs are extracted. 
  To eliminate redundancy among transcriptional variants, duplicated entries were removed using a custom script *`remove_duplicates.py`*. 
  Subsequently, the TEs which overlapped with TSSs (TE-TSS) were intersected and quantified based on their class and subfamily using another custom script *`Count_transcript_bed_all.py`*.
  ### Downstream Genes Associated with Transposable Elements
   TSS of each transcript was extracted from GTF file and converted to BED file with *`GFF2BED_TSS.py`* then TSSs that overlapped with TEs were extracted. After that, generated BED file are compared with BED file of TEs (like RepeatMasker) and TSSs which overlap with TEs are extracted. 
 TSSs that overlapped with TEs were extracted using BEDtools intersect (https://bedtools.readthedocs.io/en/latest/, v2.31.1) Then the BED file containing all TSSs overlapped with TE was compared against the original GTF file to identify candidate chimeric transcripts with *`filter_gtf_by_bed_250403.py`*.

## Requirements
- Python (v3.13 or later)
- BEDTools (v2.31 or later)
## Workflow

## Usage
  #### Step 1. Extraction of TSSs that overlapped with TEs.  
```bash
python `GFF2BED_TSS.py` original.gtf TSS.bed
```
```bash
bedtools intersect -wa TSS.bed -wb TE.bed > TSS_overlap_TE.bed
```
### TEs as Promoters 
  #### Step 2. Remove overlaps.
```bash
python remove_duplicates.py TSS_overlap_TE.bed TSS_overlap_TE.unique.bed
```
  #### Step 3. Count and atatch information about TE class, subclass and repeatname.
Count_transcript_bed_all.py TSS_overlap_TE.unique.bed TSS_overlap_TE.unique.count.bed

### Downstream Genes Associated with Transposable Elements
  #### Step 2. Compared bed file generated in Step 1. against the original GTF file.
```bash
python filter_gtf_by_bed_250403.py TSS_overlap_TE.bed original.gtf TSS_overlap_TE.gtf
```

## Licence
  It is free software; you can redistribute it and/or modify them under the MIT License.
  If you use this code in your research, please cite:
