"""
.. module:: main_convert_APS_13BM.py
   :platform: Unix
   :synopsis: Convert APS 13-BM SPE files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from dataio.data_convert import Convert

import numpy as np
import os
import scipy
import re

import logging
logging.basicConfig(filename='convert_Diamond_I12.log',level=logging.DEBUG)

def main():

    file_name = '/local/data/databank/Diamond/projections_13429.hdf'
    hdf5_file_name = '/local/data/databank/dataExchange/microCT/Diamond.h5'

    verbose = True

    print "Input files base name: ", file_name
    print "Output data exchange file name: ", hdf5_file_name

    mydata = Convert()
    # Create minimal hdf5 file
    if verbose: print "Reading data ... "
    mydata.nexus(file_name,
                        hdf5_file_name = hdf5_file_name,
                        projections_start=20,
                        projections_end=1820,
                        projections_step=1,
                        white_start=11,
                        white_end=20,
                        dark_start=1,
                        dark_end=3,
                        sample_name = 'unknown'
                   )
    if verbose: print "Done reading data ... "
    
    # Add extra metadata if available

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'Diamond I12'}) )

    ### Create HDF5 subgroup
    ### /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': "Diamond Light Source"},
                                        date_time={'value': "2013-11-30T19:17:04+0100"},
                                        beamline={'value': "JEEP I12"},
                                        )
    )

    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Michael Drakopoulos"},
                                                role={'value':"Project PI"},
                    )
        )

    f.close()
    print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

