# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_26ID.py
   :platform: Unix
   :synopsis: import APS 26-ID TIFF files (from TXM) in data exchange.

Example on how to use the `series_of_images`_ module to read APS 26-ID TIFF files (from TXM) raw tomographic data and reconstruct with tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx


def main():

    file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1/Image_raw_.tif'
#   white is saturated
#    white_file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1/Image_bg_.tif'

    projections_start = 0
    projections_end = 180
#    white_start = 0
#    white_end = 1

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 290    
#    slices_end = 294    

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 380    
    slices_end = 384    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
#                                                       white_file_name = white_file_name,                                                       
#                                                       white_start = white_start,
#                                                       white_end = white_end,
                                                       projections_digits = 3,
                                                       projections_zeros = False,
                                                       white_zeros = False,
                                                       dtype='uint8',
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
    d.center=510.0
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/APS_26_ID_', axis=0)

if __name__ == "__main__":
    main()

