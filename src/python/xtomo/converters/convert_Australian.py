# -*- coding: utf-8 -*-
"""
.. module:: main_convert_Australian.py
   :platform: Unix
   :synopsis: Convert Australian Synchrotron facility TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import xtomo.xtomo_importer as dx

def main():

    file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/SAMPLE_T_.tif'
    dark_file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/DF__AFTER_.tif'
    white_file_name = '/local/dataraid/databank/AS/Mayo_tooth_AS/BG__BEFORE_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Australian_01.h5'
    sample_name = 'Teeth'

    projections_start = 0
    projections_end = 1801
    white_start = 0
    white_end = 10
    white_step = 1
    dark_start = 0
    dark_end = 10
    dark_step = 1

    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            #hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            dark_file_name = dark_file_name,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            dark_step = dark_step,
                            sample_name = sample_name,
                            projections_digits = 4,
                            white_digits = 2,
                            dark_digits = 2,
                            projections_zeros = True,
                            log='INFO'
                            )
     

if __name__ == "__main__":
    main()

