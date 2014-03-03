# -*- coding: utf-8 -*-
"""
.. module:: convert_Elettra.py
   :platform: Unix
   :synopsis: Convert Elettra Synchrotron facility, 12bit tiff compressed data LZV method, c files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import data_exchange as dx

def main():

    file_name = '/Users/decarlo/data/elettra/Volcanic_rock/tomo_.tif'
    dark_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/dark_.tif'
    white_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/flat_.tif'

    hdf5_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/elettra_Volcanic_rock_03.h5'

    projections_start = 1
    projections_end = 1441
    white_start = 1
    white_end = 11
    white_step = 1
    dark_start = 1
    dark_end = 11
    dark_step = 1

    sample_name = 'Volcanic_rock'

    mydata = dx.Convert()
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            projections_digits = 4,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            dark_file_name = dark_file_name,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            dark_step = dark_step,
                            data_type =  'compressed_tiff', # comment this line if regular tiff
                            projections_zeros = True,
                            white_zeros = False,
                            dark_zeros = False,
                            sample_name = sample_name,
                            log='ERROR'
                            )

if __name__ == "__main__":
    main()

