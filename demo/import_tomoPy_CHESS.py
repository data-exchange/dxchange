# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_CHESS.py
   :platform: Unix
   :synopsis: Import CHESS TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read CHESS TIFF raw tomographic data and reconstruct with tomoPy

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

    file_name = '/local/dataraid/databank/CHESS/scan1/scan1_.tiff'
    dark_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_dark_.tiff'
    white_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_white_.tiff'

    projections_start = 1
    projections_end = 361
    white_start = 0
    white_end = 1
    white_step = 1
    dark_start = 0
    dark_end = 1
    dark_step = 1


    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 400    
    slices_end = 404    

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       projections_digits = 3,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                    )    

    # Xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=1160.5
    d.gridrec()

    # Write to stack of TIFFs.
    write = dataexchange.Export()
    write.xtomo_tiff(data = d.data_recon, output_file = 'tmp/CHESS_tiff_2_tomoPy_', axis=0)

if __name__ == "__main__":
    main()

