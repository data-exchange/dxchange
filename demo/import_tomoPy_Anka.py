# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_Anka.py
   :platform: Unix
   :synopsis: reconstruct ANKA Synchrotron Facility data with TomoPy
   :INPUT
       series of tiff or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx


def main():
    # read a series of tiff
    file_name = '/media/DISK_01/databank/Anka/radios/image_.tif'
    dark_file_name = '/media/DISK_01/databank/Anka/darks/image_.tif'
    white_file_name = '/media/DISK_01/databank/Anka/flats/image_.tif'

    hdf5_file_name = '/media/DISK_01/databank/dataExchange/microCT/Anka_test.h5'

    projections_start = 0
    projections_end = 3167
    white_start = 0
    white_end = 100
    dark_start = 0
    dark_end = 100

    sample_name = 'Anka'

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    
    slices_start = 800    
    slices_end = 811    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       sample_name = sample_name,
                                                       projections_digits = 5,
                                                       log='INFO'
                                                       )

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=993.825
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/ANKA_LAST', axis=0)

if __name__ == "__main__":
    main()

