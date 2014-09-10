# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_Anka.py
   :platform: Unix
   :synopsis: Import Anka TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read Anka TIFF raw tomographic data and reconstruct using tomoPy

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

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


def main():
    # read a series of tiff
    file_name = '/local/dataraid/databank/Anka/radios/image_.tif'
    dark_file_name = '/local/dataraid/databank/Anka/darks/image_.tif'
    white_file_name = '/local/dataraid/databank/Anka/flats/image_.tif'

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
    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
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
    mydata = ex.Export()
    mydata.xtomo_tiff(data = d.data_recon, output_file = 'tmp/Anka_tiff_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()

