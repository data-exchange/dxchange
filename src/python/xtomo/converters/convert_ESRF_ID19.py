# -*- coding: utf-8 -*-
"""
.. module:: main_convert_esrf.py
   :platform: Unix
   :synopsis: Convert esrf ID-19 edf files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import xtomo.xtomo_importer as dx

def main():

    file_name = '/local/dataraid/databank/ESRF/scan.edf'
    dark_file_name = '/local/dataraid/databank/ESRF/dark.edf'
    white_file_name = '/local/dataraid/databank/ESRF/flat.edf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/ESRF.h5'

    sample_name = 'esrf'

    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.stack(file_name,
                 #hdf5_file_name = hdf5_file_name,
                 white_file_name = white_file_name,
                 dark_file_name = dark_file_name,
                 projections_data_type = 'edf',
                 white_data_type = 'edf',
                 dark_data_type = 'edf',
                 sample_name = sample_name,
                 log='INFO'
                 )

if __name__ == "__main__":
    main()

