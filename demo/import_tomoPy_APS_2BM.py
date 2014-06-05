# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_2BM.py
   :platform: Unix
   :synopsis: reconstruct APS 2-BM hdf4 data with TomoPy
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
    log_file = '/local/dataraid/databank/APS_2_BM/Sam18_hornby/Sam18_exp.hdf'

    #Read APS 2-BM log file data
    f = SD.SD(log_file)

    sds = f.select('base_name')
    data = sds.get()
    base_name = ''.join(data)
    print base_name

    file_name = os.path.split(log_file)[0] + "/" + "raw" + "/" + base_name + "_.hdf"
     
    sds = f.select('start_angle')
    start_angle = sds.get()[0]

    sds = f.select('end_angle')
    end_angle = sds.get()[0]

    sds = f.select('angle_interval')
    angle_interval = sds.get()[0]

    sds = f.select('num_dark_fields')
    num_dark_fields = sds.get()[0]

    f.end()
    
    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = projections_start + (int)((end_angle -  start_angle) / angle_interval) + 1
    dark_start = projections_end + 1 
    dark_end = dark_start + num_dark_fields

    sample_name = base_name

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
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 5,
                                                       data_type = 'hdf4',
                                                       log='INFO'
                                                       )

##    # if you have already created a data exchange file using convert_APS_2BM.py module,
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
    d.center=1023.4
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/APS_2_BM_', axis=0)

if __name__ == "__main__":
    main()

