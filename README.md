# synplot.py

Draw gene synteny from gff files to svg output.

## Description
Simple script to draw gene architecture of one or several species/strains. Provide one or more gff files, and get output in svg format for flexible postprocessing.

## Usage
```bash
python synplot.py -g annotation1.gff[,annotation2.gff,...,annotationN.gff]
```
Annotation files need to be in gff format. Genes names should be specified in the "Note" gff tag (e.g. Note=BtubA).

## Highlights
* Plot synteny directly from a gff file. Just extract the region of interest from your whole-genome gff's.
* Output is written to svg format, for easy postprocessing.
