# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_15ID.py
   :platform: Unix
   :synopsis: reconstruct APS 15-ID hdf4 data with TomoPy
   :INPUT
       APS 2_BM exp file or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from pyhdf import SD
import os

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re

def main():

    file_name = '/local/dataraid/databank/APS_15_ID/AluminaStick_0A_fullRunRenamed/AluminaStick_.hdf'
    hdf5_file_name = '/local/dataraid/databank/APS_15_ID/AluminaStick_0A_fullRunRenamed/AluminaStick_00.h5'
    
    projections_start = 1
    projections_end = 361

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()

    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       projections_digits = 4,
                                                       data_type = 'hdf5',
                                                       log='INFO'
                                                       )

##    # if you have already created a data exchange file using convert_APS_15ID.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
##
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Hornby_19keV_10x_APS_2011_01.h5'
##    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
##                                                   slices_start=0,
##                                                   slices_end=2)

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=772.2
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/AluminaStick_0A_fullRunRenamed_', axis=0)

if __name__ == "__main__":
    main()

