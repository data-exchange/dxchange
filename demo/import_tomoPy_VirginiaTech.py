# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_VirginiaTech.py
   :platform: Unix
   :synopsis: reconstruct tiff files or data exchange data with TomoPy
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
    file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4_.tif'
    dark_file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4postDark_.tif'
    white_file_name = '/local/dataraid/databank/VirginiaTech/test_sample_Diplo_4/Diplodocus_1_200mm_4postFlat_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/VirginiaTech_test.h5'
    sample_name = 'Diplodocus_1_200mm_'

    projections_start = 0
    projections_end = 1500
    white_start = 0
    white_end = 10
    white_step = 1
    dark_start = 0
    dark_end = 10
    dark_step = 1

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    
    slices_start = 600    
    slices_end = 604    

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
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       sample_name = sample_name,
                                                       projections_digits = 5,
                                                       projections_zeros = True,
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
    d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    #d.center=1010.0
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/VT_', axis=0)

if __name__ == "__main__":
    main()

