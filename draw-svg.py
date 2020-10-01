#!/usr/bin/env python
# -*- coding: utf-8 -*-

import drawSvg as draw
from matplotlib.pyplot import cm
import matplotlib.colors
import argparse

parser = argparse.ArgumentParser("Draw gene synteny from gff files.")
parser.add_argument("-g","--gff", help="Comma-separated list of gff files to plot.", type = str)
parser.add_argument("-P","--Pastel", help="Matplotlib pastel for coloring. [Pastel1]", type = str, default = "Pastel1")
args = parser.parse_args()

def readGff(gff):
    '''Read a gff file into memory.
    '''
    genes = []
    min,max = 0, 0
    with open(gff, "r") as in_gff:
        for line in in_gff:
            line = line.strip()
            fields = line.split("\t")

            if fields[2] == "gene":
                if "Note=" in line:
                    note = [f for f in fields[8].split(";") if f.startswith("Note=")][0].strip("Note=")
                    genes.append((fields[0], int(fields[3]), int(fields[4]), fields[6], note))
                else:
                    genes.append((fields[0], int(fields[3]), int(fields[4]), fields[6], "hypothetical_protein"))
                if min == 0:
                    min = int(fields[3])
                max = int(fields[4])
    return genes, min, max

def draw_genes(annotations, scale, color_table):
    '''Draw the genes in annotations.
    '''
    # Define the coordinate system to draw on.
    # x length is fixed, y depends on how many species/strains are in the
    # annotations (how many gff's were given to the script)
    y_len = 25*len(annotations) + 50 # Add 50 for the scale bar
    d = draw.Drawing(500, y_len, origin = (0,0), displayInline=False)

    for idx, (k, v) in enumerate(annotations.items()):
        genes, min, max = v[0], v[1], v[2]
        contig_length = (max - min)*scale
        offset = 30
        row = y_len-25*(idx+1)

        # Draw a line for each gff file and it's name
        d.append(draw.Line(offset, row, contig_length+offset, row, stroke='black', stroke_width=2, fill='none'))
        d.append(draw.Text(k[:10],6, 2, row-1, text_anchor="left", fill='black'))

        for gene in genes:
            color = color_table[gene[4]]
            arrow = draw.Marker(0, -0.5, 1, 0.5, scale=2, orient='auto')
            arrow.append(draw.Lines(0, -0.5, 0, 0.5, 1, 0, fill=color, close=True))

            print(gene)

            # Normalize gene position and reverse genes
            # TODO: make sure orientations don't change when scaling makes
            # 12 too high
            if gene[3] == "+":
                gene_coords = ((gene[1] - min)*scale+offset, \
                                (gene[2] - min)*scale+offset)
                                #(gene[2] - min)*scale+offset-12)
                arrow_positions = range(int(gene_coords[0])+3, \
                                    int(gene_coords[1])-3, int(700*scale))
                k = -1

            else:
                gene_coords = ((gene[2] - min)*scale+offset, \
                                (gene[1] - min)*scale+offset)
                                #(gene[1] - min)*scale+offset+12)
                arrow_positions = range(int(gene_coords[1]+3), \
                                    int(gene_coords[0]-3), int(700*scale))
                k = 1
            print(gene_coords)
            print(arrow_positions)

            # Draw an arrow for each gene
            d.append(draw.Line(gene_coords[0], row, gene_coords[1], row, \
                        stroke=color, stroke_width=6, fill='none'))#, \
                        #marker_end=arrow))
            for a in arrow_positions:
                d.append(draw.Lines(a+2*k, row+2, a, row, a+2*k, row-2, \
                        stroke_width=0.2, stroke = "black",fill="none"))

            ## Draw labels
            # Gene name, skip hypothetical proteins
            if gene[4] != "hypothetical_protein":
                text_pos = gene_coords[0] + (gene_coords[1]-gene_coords[0])/2
                d.append(draw.Text(gene[4],5, text_pos,row-10, center=0.6, text_anchor="middle", fill='black'))

    # Draw a scale bar
    longest = int(450 / scale)
    row = 25
    d.append(draw.Line(offset, row, longest, row, stroke='black', stroke_width=1, fill='none'))
    for num in range(0,longest, 1000):
        scaled_num = num*scale + offset
        d.append(draw.Line(scaled_num, row+1.5, scaled_num, row-1.5, stroke='black', stroke_width=0.5, fill='none'))
        d.append(draw.Text(str(num), 3, scaled_num, row-5, center=True, fill='black'))

    d.setPixelScale(2)
    d.saveSvg('test.svg')

def color_genes(annotations):
    color_table = {}
    idx = 0
    for v in annotations.values():
        for gene in v[0]:
            if gene[4] not in color_table.keys():
                c = matplotlib.colors.rgb2hex(cm.Pastel2(idx)[:3])
                idx += 1
                color_table[gene[4]] = c

    # hypothetical_proteins are hard coded to grey
    color_table["hypothetical_protein"] = "#c2c2c2"
    return color_table

def findScale(annotations):
    '''Find a good scaling factor for drawing the svg. How much to downscale
    depends on the longest distance with annotated genes that is in the gff files
    provided to the script.
    '''
    distances = [v[2] - v[1] for v in annotations.values()]
    longest = max(distances)

    # x distance of the drawing coordinate system is fixed to 500
    # We need some space on the sides, for text etc.
    scale = 450 / longest
    return scale


def main():
    gffs = args.gff.split(",")
    annotations = {}
    for gff in gffs:
        fname = gff.strip(".gff")
        annotations[fname] = (readGff(gff))

    scale = findScale(annotations)
    color_table = color_genes(annotations)

    draw_genes(annotations, scale, color_table)

if __name__ == "__main__":
    main()
