# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_APS_26ID.py
   :platform: Unix
   :synopsis: import APS 26-ID TIFF files (from TXM) in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 26-ID TIFF files (from TXM) raw tomographic data and reconstruct with tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

def main():

    file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1_TomoScript_181imgs_p1s_b1.txrm'
    # white is saturated .... 
    white_file_name = '/local/dataraid/databank/TXM_26_ID/20130731_001_Background_Reference_20imgs_p5s_b1.xrm'
    sample_name = '20130731_004_Stripe_Solder_Sample_Tip1'

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 620    
    slices_end = 624    

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                        white_file_name = white_file_name, 
                                                        slices_start = slices_start, 
                                                        slices_end = slices_end, 
                                                        data_type='xradia', 
                                                        log='INFO')
    print "data:", data.shape, data.dtype
    print "white:", white.shape, white.dtype
    print "dark:", dark.shape, dark.dtype
    print "theta:", theta.shape, theta.dtype

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    d.center=510.0
    d.gridrec()

    # Write to stack of TIFFs.
    write = dataexchange.Export()
    write.xtomo_tiff(data = d.data_recon, output_file = 'tmp/APS_26_ID_xradia_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()

