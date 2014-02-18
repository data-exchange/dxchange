# -*- coding: utf-8 -*-
"""
.. module:: main_convert_Australian.py
   :platform: Unix
   :synopsis: Convert Australian Synchrotron facility TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from dataio.data_convert import Convert

import re

import logging
logging.basicConfig(filename='convert_Australian.log',level=logging.DEBUG)

import PIL.Image as Image
from dataio.elettra.tifffile import TiffFile

def main():

##    file_name = '/local/data/databank/elettra/Volcanic_rock/tomo/tomo_0001.tif'
##    tif = TiffFile(file_name)
##    print tif
    
##    im = Image.open(file_name)

    file_name = '/local/data/databank/elettra/Volcanic_rock/tomo/tomo_.tif'
    hdf5_file_name = '/local/data/databank/elettra/Volcanic_rock/elettra.h5'
    projections_start = 1
    projections_end = 6
    mydata = Convert()
    mydata.series_of_images(file_name,
                     hdf5_file_name,
                     projections_start,
                     projections_end,
                     projections_digits = 4,
                     data_type =  'compressed_tiff',
                     zeros = True,
                     verbose = False
                     )

##    dark_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/tomo/dark_.tif'
##    white_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/tomo/flat_.tif'
##    hdf5_file_name = '/Users/decarlo/data/elettra/elettra.h5'
##    sample_name = 'Teeth'
##
##    projections_start = 1
##    projections_end = 6
##    white_start = 1
##    white_end = 6
##    white_step = 1
##    dark_start = 1
##    dark_end = 6
##    dark_step = 1
##
##    verbose = True
##
##    if verbose: print "Input projection base name: ", file_name
##    if verbose: print "Input white base name: ", white_file_name
##    if verbose: print "Input dark base name: ", dark_file_name
##    if verbose: print "Output data exchange file name: ", hdf5_file_name
##
##    mydata = Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                     hdf5_file_name,
##                     projections_start,
##                     projections_end,
##                     white_file_name = white_file_name,
##                     white_start = white_start,
##                     white_end = white_end,
##                     white_step = white_step,
##                     dark_file_name = dark_file_name,
##                     dark_start = dark_start,
##                     dark_end = dark_end,
##                     dark_step = dark_step,
##                     sample_name = sample_name,
##                     projections_digits = 4,
##                     white_digits = 1,
##                     dark_digits = 1,
##                     zeros = True,
##                     verbose = False
##                     )
##    if verbose: print "Done reading data ... "
##     
##    # Add extra metadata if available
##
##    # Open DataExchange file
##    f = DataExchangeFile(hdf5_file_name, mode='a') 
##
##    # Create HDF5 subgroup
##    # /measurement/instrument
##    f.add_entry( DataExchangeEntry.instrument(name={'value': 'Elettra Synchrotron Facility'}) )
##
##    # Create HDF5 subgroup
##    # /measurement/instrument/source
##    f.add_entry( DataExchangeEntry.source(name={'value': 'Elettra Synchrotron FacilityI'},
##                                        date_time={'value': "2013-10-19T22:22:13+0100"},
##                                        beamline={'value': "SYRMEP"},
##                                        )
##    )
##
##    # /measurement/experimenter
##    f.add_entry( DataExchangeEntry.experimenter(name={'value':"SYRMEP"},
##                                                role={'value':"Project PI"},
##                    )
##        )
##
##    f.close()
##    if verbose: print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

