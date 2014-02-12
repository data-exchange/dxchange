# -*- coding: utf-8 -*-
"""
.. module:: main_convert_esrf.py
   :platform: Unix
   :synopsis: Convert esrf ID-19 edf files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from dataio.data_convert import Convert
from dataio.esrf.EdfFile import EdfFile
import numpy as np

import re
import logging
logging.basicConfig(filename='convert_esrf.log',level=logging.DEBUG)

def main():

    file_name = '//local/data/esrf/scan.edf'
    dark_file_name = '/local/data/esrf/dark.edf'
    white_file_name = '/local/data/esrf/flat.edf'
    hdf5_file_name = '/local/data/esrf_test.h5'
    sample_name = 'esrf'

    verbose = True

    if verbose: print file_name
    if verbose: print white_file_name
    if verbose: print hdf5_file_name
#    if verbose: print log_file

    mydata = Convert()
    # Create minimal hdf5 file
    if verbose: print "Reading data ... "
    mydata.stack(file_name,
                   hdf5_file_name = hdf5_file_name,
                   white_file_name = white_file_name,
                   dark_file_name = dark_file_name,
                   projections_data_type = 'edf',
                   white_data_type = 'edf',
                   dark_data_type = 'edf',
                   sample_name = sample_name
                   )
    if verbose: print "Done reading data ... "

     
    # Add extra metadata if available

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'ESRF'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': 'ESRF'},
                                        date_time={'value': "2014-12-05T19:42:13+0100"},
                                        beamline={'value': "ID-19"},
                                        )
    )

    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Emmanuelle"},
                                                role={'value':"Project PI"},
                    )
        )

    f.close()
    if verbose: print "Done converting ", file_name

if __name__ == "__main__":
    main()

