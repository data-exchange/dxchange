# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_NSLS.py
   :platform: Unix
   :synopsis: reconstruct NSLS data with TomoPy
   :INPUT
       series of tiff and log file or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/rad_0400ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/ff_0350ms_.tiff'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/NSLS.h5'

    white_start = 0
    white_end = 2580
    white_step = 30
    projections_start = 0
    projections_end = 2600

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_digits=4,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       log='INFO'
                                                       )
s
    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=1010.0
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/SLS_', axis=0)

if __name__ == "__main__":
    main()

