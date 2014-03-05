# -*- coding: utf-8 -*-
"""
.. module:: main_convert_NSLS.py
   :platform: Unix
   :synopsis: Convert NSLS TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx

## NOT CHECKED

def main():

    file_name = '/local/data/databank/NSLS/middle/rad_1000ms_.tiff'
    #dark_file_name = '/local/data/databank/NSLS/middle/'
    white_file_name = '/local/data/databank/NSLS/middle/ff_0800ms_.tiff'

    hdf5_file_name = '/local/data/databank/dataExchange/microCT/NSLS_06.h5'

    white_start = 0
    white_end = 1200
    white_step = 30
    projections_start = 0
    projections_end = 1200

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            # dark_file_name = dark_file_name,
                            # dark_start = dark_start,
                            # dark_end = dark_end,
                            # dark_step = dark_step,
                            # projections_digits = 4,
                            log='WARNING'
                            )

     
if __name__ == "__main__":
    main()

