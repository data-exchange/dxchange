# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_PetraIII.py
   :platform: Unix
   :synopsis: Import Petra III P05 and P06 TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read  Petra III P05 and P06 TIFF raw tomographic data and recostruct with tomoPy

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
    # read a series of tiff

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 0 -> 19
    file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0002/ccd/pco01/ccd_.tif'
    dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0000/ccd/pco01/ccd_.tif'
    white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0001/ccd/pco01/ccd_.tif'

    projections_start = 0
    projections_end = 1441
    white_start = 0
    white_end = 20
    white_step = 1
    dark_start = 0
    dark_end = 20
    dark_step = 1

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    slices_start = 1000    
    slices_end = 1004    

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       #projections_angle_range=360,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       projections_digits = 4,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                       )


    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval(pixel_size=0.9e-4, dist=6.9, energy=15.25)
    #d.correct_drift()
    d.center=1872.87890625
    d.gridrec()

    # Write to stack of TIFFs.
    write = dataexchange.Export()
    write.xtomo_tiff(data = d.data_recon, output_file = 'tmp/PetraIII_tiff_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()

