# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_SLS.py
   :platform: Unix
   :synopsis: reconstruct SLS Tomcat data with TomoPy
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
    file_name = '/local/dataraid/databank/SRC/read_data/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_1700.969cm-1.dpt'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/SRC_2500_50_50_1700.969_01.h5'

    sample_name = 'test'


    
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 76    
    slices_end = 77    

#    mydata = dx.Import()
#    # Read series of images
#    data, white, dark, theta = mydata.series_of_images(file_name,
#                                                       sample_name = sample_name,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
#                                                       data_type='dpt',
#                                                       log='INFO'
#                                                       )

##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
                                                   slices_start=slices_start,
                                                   slices_end=slices_end)

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=53
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/SLC_', axis=0)

if __name__ == "__main__":
    main()

