# synplot.py

Draw gene synteny from gff files to svg output.

## Description
Simple script to draw gene architecture of one or several species/strains. Provide one or more gff files, and get output in svg format for flexible postprocessing.

## Usage
```bash
python synplot.py -g annotation1.gff[,annotation2.gff,...,annotationN.gff]
```
Annotation files need to be in gff format. Extract the region of interest from your gff file(s) prior to usage. Genes names should be specified in the "Note" gff tag (e.g. Note=BtubA). Genes with the same name will be given the same color, genes annotated as "hypothetical_protein" or without functional annotation will be grey.

## Highlights
* Plot synteny directly from a gff file.
* Output is written to svg format for easy postprocessing with e.g. [Inkscape](https://inkscape.org/release/inkscape-1.0.1/).

## Example
![Example](/example.svg)
