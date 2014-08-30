# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_Elettra.py
   :platform: Unix
   :synopsis: Import Elettra TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read Elettra TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples

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
    # read a series of tiff
    file_name = '/local/dataraid/databank/Elettra/Volcanic_rock/tomo_.tif'
    dark_file_name = '/local/dataraid/databank/Elettra/Volcanic_rock/dark_.tif'
    white_file_name = '/local/dataraid/databank/Elettra/Volcanic_rock/flat_.tif'

    projections_start = 1
    projections_end = 1441
    white_start = 1
    white_end = 11
    white_step = 1
    dark_start = 1
    dark_end = 11
    dark_step = 1
    
    sample_name = 'Volcanic_rock'

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    
    slices_start = 150    
    slices_end = 154    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_digits = 4,
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
                                                       data_type =  'compressed_tiff', # comment this line if regular tiff
                                                       projections_zeros = True,
                                                       white_zeros = False,
                                                       dark_zeros = False,
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
    d.center=1096.375
    d.gridrec()

    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/Elettra_', axis=0)

if __name__ == "__main__":
    main()

