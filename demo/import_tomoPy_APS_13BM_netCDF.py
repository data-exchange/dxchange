# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_13BM_netCDF.py
   :platform: Unix
   :synopsis: reconstruct APS 13-BM netCDF data with TomoPy
   :INPUT
       series of netCDF files or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    # read a series of netCDF
    file_name = '/local/dataraid/databank/APS_13_BM/NC/Dorthe_F_.nc'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/APS_13_BM_NC_test_02.h5'

    white_start = 1
    white_end = 4
    white_step = 2
    projections_start = 2
    projections_end = 3
    projections_step = 1

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 300    
    slices_end = 304    

    mydata = dx.Import()    
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_step = projections_step,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       projections_digits = 3,
                                                       data_type='nc',
                                                       log='INFO'
                                                       )

##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
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
    d.center=484.5
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/APS_13BM_', axis=0)

if __name__ == "__main__":
    main()

