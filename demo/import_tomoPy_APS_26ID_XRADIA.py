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

    file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1_TomoScript_181imgs_p1s_b1.txrm'
    # white is saturated .... 
    # white_file_name = '/local/dataraid/databank/TXM_26_ID/20130731_001_Background_Reference_20imgs_p5s_b1.xrm'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/APS_26_ID_XRADIA.h5'
    sample_name = '20130731_004_Stripe_Solder_Sample_Tip1'


    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       white_file_name = white_file_name,                                                       
                                                       data_type='xradia',
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

