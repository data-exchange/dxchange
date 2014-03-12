# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_2BM.py
   :platform: Unix
   :synopsis: Convert APS 2-BM HDF4 files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx

def main():

    file_name = '/local/dataraid/databank/APS_2_BM/Sam18_hornby/raw/Hornby_19keV_10x_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Hornby_19keV_10x_APS_2011_01.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )
if __name__ == "__main__":
    main()

