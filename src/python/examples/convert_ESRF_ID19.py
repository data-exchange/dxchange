# -*- coding: utf-8 -*-
"""
.. module:: main_convert_esrf.py
   :platform: Unix
   :synopsis: Convert esrf ID-19 edf files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx

def main():

    file_name = '/local/data/ESRF/scan.edf'
    dark_file_name = '/local/data/ESRF/dark.edf'
    white_file_name = '/local/data/ESRF/flat.edf'
    hdf5_file_name = '/local/data/ESRF/esrf_01.h5'

    sample_name = 'esrf'

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.stack(file_name,
                 hdf5_file_name = hdf5_file_name,
                 white_file_name = white_file_name,
                 dark_file_name = dark_file_name,
                 projections_data_type = 'edf',
                 white_data_type = 'edf',
                 dark_data_type = 'edf',
                 sample_name = sample_name,
                 log='ERROR'
                 )

if __name__ == "__main__":
    main()

