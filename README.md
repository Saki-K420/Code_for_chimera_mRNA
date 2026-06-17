Code_for_chimera_mRNA
========================
## Overview
  `Code_for_chimera_mRNA` is a pipeline to detect "chimeric mRNAs", which are derived from Transposable element (TE). Methods for detecting chimeric mRNAs are not yet standardized. This repository include sequence of custom Python scripts for identifying potential chimeric mRNAs. 
  The workflow can be broadly divided into two categories:
### TEs as Promoters
### Downstream Genes Associated with Transposable Elements
   In this pipeline, transcription start sites (TSSs) are defined as the first nucleotide of each mRNA transcript. 
## Description
  TSS of each transcript was extracted from GTF file and converted to BED file with *`GFF2BED_TSS.py`* then TSSs that overlapped with TEs were extracted.  
  ### TEs as Promoters 
  To eliminate redundancy among transcriptional variants, duplicated entries were removed using a custom script *`remove_duplicates.py`*. 
  Subsequently, the TEs which overlapped with TSSs (TE-TSS) were intersected and quantified based on their class and subfamily using another custom script *`Count_transcript_bed_all.py`*.
  ### Downstream Genes Associated with Transposable Elements
 TSSs that overlapped with TEs were extracted using BEDtools intersect (https://bedtools.readthedocs.io/en/latest/, v2.31.1) Then the BED file containing all TSSs overlapped with TE was compared against the original GTF file to identify candidate chimeric transcripts with *`filter_gtf_by_bed_250403.py`*.

## Demo

## Usage

## Install

## Licence
  It is free software; you can redistribute it and/or modify them under the MIT License.
  If you use this code in your research, please cite:
