# -*- coding: utf-8 -*-
"""
.. module:: convert_Anka.py
   :platform: Unix
   :synopsis: Convert Anka TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>

""" 

import xtomo.xtomo_importer as dx

import re

def main():

    file_name = '/local/dataraid/databank/Anka/radios/image_.tif'
    dark_file_name = '/local/dataraid/databank/Anka/darks/image_.tif'
    white_file_name = '/local/dataraid/databank/Anka/flats/image_.tif'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Anka_01.h5'

    projections_start = 0
    projections_end = 3167
    white_start = 0
    white_end = 100
    dark_start = 0
    dark_end = 100

    sample_name = 'Anka'
    
    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                     #hdf5_file_name = hdf5_file_name,
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
                     log='INFO'
                     )

if __name__ == "__main__":
    main()

