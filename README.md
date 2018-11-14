# PPI-Relation-Extraction-Py
# Biocreative VI Track 4 task - Extract protein interactions affected by mutation 
## Introduction
We used a co-occurrence based approach to extract protein interactions affected by mutation (PPIm) .  We applied a heuristic that if a gene pair gets mentioned in more than two sentences within an abstract then the pair is likely to be in a PPIm relationship. This heuristic was based on the fact that all the documents in the training set are relevant for PPIm, as they were all marked as relevant in the document triage task training set.  

## Method
GNormPlus (docker https://hub.docker.com/r/lanax/gnormplus/)  was used for protein names extraction and normalization. Ling sentence extractor was used to extract sentences from the abstracts. In the relation extraction phase, If any pair of genes identified within the document co-occurred in more than two sentences within the same document then it was identified as a valid PPIm relationship.

## Results
The gene recognition and normalization phase using GNormPlus had a F-score of 40.6%, with a recall of 53.4 % in the full training set.   The relation extraction phase has a precision of 30.757 %, recall of 24.735 % resulting in an F-score of 27.419%

