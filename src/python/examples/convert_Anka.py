# -*- coding: utf-8 -*-
"""
.. module:: convert_Anka.py
   :platform: Unix
   :synopsis: Convert Anka TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx

import re

def main():

    file_name = '/Users/decarlo/data/databank/Anka/radios/image_.tif'
    dark_file_name = '/Users/decarlo/data/databank/Anka/darks/image_.tif'
    white_file_name = '/Users/decarlo/data/databank/Anka/flats/image_.tif'

    hdf5_file_name = '/Users/decarlo/data/databank/dataExchange/microCT/Anka_04.h5'

    projections_start = 0
    projections_end = 11
    white_start = 0
    white_end = 12
    dark_start = 0
    dark_end = 13

    sample_name = 'Anka'
    
    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                     hdf5_file_name = hdf5_file_name,
                     projections_start = projections_start,
                     projections_end = projections_end,
                     white_file_name = white_file_name,
                     white_start = white_start,
                     white_end = white_end,
                     dark_file_name = dark_file_name,
                     dark_start = dark_start,
                     dark_end = dark_end,
                     sample_name = sample_name,
                     projections_digits = 5,
                     projections_zeros = True,
                     log='WARNING'
                     )

if __name__ == "__main__":
    main()

