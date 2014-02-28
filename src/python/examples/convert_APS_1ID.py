# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_1ID.py
   :platform: Unix
   :synopsis: Convert APS 1-ID TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from data_exchange.data_convert import Convert

import re

import logging
logging.basicConfig(filename='convert_APS_1ID.log',level=logging.DEBUG)

def main():

    file_name = '/local/data/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_.tif'
    log_file = '/local/data/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_TomoStillScan.dat'

    hdf5_file_name = '/local/data/databank/dataExchange/microCT/CAT4B_2.h5'

    projections_start = 943
    projections_end = 1853
    white_start = 1844
    white_end = 1853
    dark_start = 1854
    dark_end = 1863

    mydata = Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                     hdf5_file_name,
                     projections_start,
                     projections_end,
                     white_start = white_start,
                     white_end = white_end,
                     dark_start = dark_start,
                     dark_end = dark_end,
                     projections_digits = 6,
                     verbose = False
                     )

     
    # Add extra metadata if available / desired

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'APS 1-ID Tomography'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': 'Advanced Photon Source'},
                                        date_time={'value': "2012-07-08T15:42:56+0100"},
                                        beamline={'value': "1-ID"},
                                        current={'value': 100.96, 'units': 'mA', 'dataset_opts': {'dtype': 'd'}},
                                        )
    )

    # Create HDF5 subgroup
    # /measurement/instrument/monochromator
    f.add_entry( DataExchangeEntry.monochromator(type={'value': 'unknow'},
                                                energy={'value': 65, 'units': 'keV', 'dataset_opts': {'dtype': 'd'}},
                                                mono_stripe={'value': 'unknow'},
                                                )
        )

    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Peter Kenesei"},
                                                role={'value':"Project PI"},
                                                affiliation={'value':"Advanced Photon Source"},
                                                phone={'value':"+1 630 252-0133"},
                                                email={'value':"kenesei@aps.anl.gov"},

                    )
        )


    f.close()
    print "Done creating data exchange file: ", hdf5_file_name

if __name__ == "__main__":
    main()

