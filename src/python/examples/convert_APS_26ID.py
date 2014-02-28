# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_26ID.py
   :platform: Unix
   :synopsis: Convert APS 26-ID TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from data_exchange.data_convert import Convert

import re

import logging
logging.basicConfig(filename='convert_APS_26ID.log',level=logging.DEBUG)

def main():

    file_name = '/local/data/databank/TXM_26ID/Miller1/ABR_1SP_.tif'
    #dark_file_name = '/local/data/databank/AS/Mayo_tooth_AS/BG__AFTER_.tif'
    #white_file_name = '/local/data/databank/AS/Mayo_tooth_AS/BG__BEFORE_.tif'
    hdf5_file_name = '/local/data/databank/dataExchange/TXM/TXM_APS26IDMiller1.h5'
    sample_name = 'Teeth'

    projections_start = 0
    projections_end = 361
    white_start = 0
    white_end = 0
    white_step = 1
    dark_start = 0
    dark_end = 0
    dark_step = 1

    verbose = True

    if verbose: print "Input projection base name: ", file_name
    #if verbose: print "Input white base name: ", white_file_name
    #if verbose: print "Input dark base name: ", dark_file_name
    if verbose: print "Output data exchange file name: ", hdf5_file_name

    mydata = Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                     hdf5_file_name,
                     projections_start,
                     projections_end,
                     #white_file_name = white_file_name,
                     white_start = white_start,
                     white_end = white_end,
                     white_step = white_step,
                     #dark_file_name = dark_file_name,
                     #dark_start = dark_start,
                     #dark_end = dark_end,
                     #dark_step = dark_step,
                     #sample_name = sample_name,
                     projections_digits = 4,
                     #white_digits = 2,
                     #dark_digits = 2,
                     projections_zeros = True,
                     verbose = False
                     )
    if verbose: print "Done reading data ... "
     
    # Add extra metadata if available

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'Australian Synchrotron Facility'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': 'Australian Synchrotron FacilityI'},
                                        date_time={'value': "2013-10-19T22:22:13+0100"},
                                        beamline={'value': "Tomography"},
                                        )
    )

    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Sherry Mayo"},
                                                role={'value':"Project PI"},
                    )
        )

    f.close()
    if verbose: print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

