"""
.. module:: main_convert_APS_13BM.py
   :platform: Unix
   :synopsis: Convert APS 13-BM SPE files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from data_exchange.data_convert import Convert

import numpy as np
import os
import scipy
import re

import logging
logging.basicConfig(filename='convert_APS_13BM.log',level=logging.DEBUG)

def main():

    file_name = '/local/data/databank/APS_13_BM/run2_soln1_2_.SPE'
    hdf5_file_name = '/local/data/databank/dataExchange/microCT/run2_soln1_2_ZZZ.h5'

    verbose = True

    if verbose: print "Input files base name: ", file_name
    if verbose: print "Output data exchange file name: ", hdf5_file_name

    mydata = Convert()
    # Create minimal hdf5 file
    if verbose: print "Reading data ... "
    mydata.multiple_stack(file_name,
                        hdf5_file_name = hdf5_file_name,
                        projections_start=2,
                        projections_end=7,
                        projections_step=2,
                        white_start=1,
                        white_end=8,
                        white_step=2,
                        sample_name = 'Stripe_Solder_Sample_Tip1'
                   )
    if verbose: print "Done reading data ... "
    
    # Add extra metadata if available

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'APS 13-BM'}) )

    ### Create HDF5 subgroup
    ### /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': "Advanced Photon Source"},
                                        date_time={'value': "2013-11-30T19:17:04+0100"},
                                        beamline={'value': "13-BM"},
                                        )
    )

    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Mark Rivers"},
                                                role={'value':"Project PI"},
                    )
        )

    f.close()
    if verbose: print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

