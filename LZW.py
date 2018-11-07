# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 01:01:03 2018

@author: Vivian Wong Kah Ong
"""

import argparse
import sys
from LZW_functions import encoder, decoder

# --- Argument parsing ---

parser = argparse.ArgumentParser(description="LZW encoder and decoder")

# Input and Output path
parser.add_argument("-e", "--encode", action='store', default=0, type=str, dest='encode_path',help='Path of file to be compressed')
parser.add_argument("-d", "--decode", action='store', default=0, type=str, dest='decode_path',help='Path of file to be decompressed')

args = parser.parse_args()

# If no input file, print help
if args.encode_path == 0 and args.decode_path == 0:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.encode_path != 0:
    encoder(args.encode_path)

if args.decode_path != 0:
    decoder(args.decode_path)