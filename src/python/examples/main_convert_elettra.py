# -*- coding: utf-8 -*-
"""
.. module:: main_convert_Elettra.py
   :platform: Unix
   :synopsis: Convert Elettra Synchrotron facility, 12bit tiff compressed data LZV method, c files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from dataio.data_convert import Convert

import re

import logging
logging.basicConfig(filename='convert_Elettra.log',level=logging.DEBUG)

import PIL.Image as Image
from dataio.elettra.tifffile import TiffFile

def main():

    file_name = '/local/data/databank/elettra/Volcanic_rock/tomo/tomo_.tif'
    dark_file_name = '/local/data/databank/elettra/Volcanic_rock/tomo/dark_.tif'
    white_file_name = '/local/data/databank/elettra/Volcanic_rock/tomo/flat_.tif'

    hdf5_file_name = '/local/data/databank/elettra/Volcanic_rock/elettra_Volcanic_rock.h5'

    projections_start = 1
    projections_end = 482
    white_start = 1
    white_end = 10
    white_step = 1
    dark_start = 1
    dark_end = 10
    dark_step = 1

    sample_name = 'Volcanic_rock'

    mydata = Convert()
    mydata.series_of_images(file_name,
                     hdf5_file_name,
                     projections_start,
                     projections_end,
                     projections_digits = 4,
                     white_file_name = white_file_name,
                     white_start = white_start,
                     white_end = white_end,
                     white_step = white_step,
                     dark_file_name = dark_file_name,
                     dark_start = dark_start,
                     dark_end = dark_end,
                     dark_step = dark_step,
                     data_type =  'compressed_tiff',
                     projections_zeros = True,
                     white_zeros = False,
                     dark_zeros = True,
                     verbose = False,
                     sample_name = sample_name
                     )

##    dark_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/tomo/dark_.tif'
##    white_file_name = '/Users/decarlo/data/elettra/Volcanic_rock/tomo/flat_.tif'
##    hdf5_file_name = '/Users/decarlo/data/elettra/elettra.h5'
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
    verbose = True
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
##                     projections_zeros = True,
##                     verbose = False
##                     )
##    if verbose: print "Done reading data ... "
##     
    # Add extra metadata if available

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'Elettra Synchrotron Facility'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': 'Elettra Synchrotron FacilityI'},
                                        date_time={'value': "2013-10-19T22:22:13+0100"},
                                        beamline={'value': "SYRMEP"},
                                        )
    )

    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Dr. Margherita POLACCI"},
                                                role={'value':"Project PI"},
                                                affiliation={'value':"Istituto Nazionale di Geofisica e Vulcanologia"},
                                                address={'value':"via della Faggiola 32, 56126 Pisa, Italy"},
                                                phone={'value':"+390508311957"},
                                                web={'value':"http://www.pi.ingv.it/chisiamo/paginepersonali/polacci.html"},
                    )
        )

    f.close()
    if verbose: print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

