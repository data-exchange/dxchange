# -*- coding: utf-8 -*-
"""
.. module:: convert_CHESS.py
   :platform: Unix
   :synopsis: Convert CHESS TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read CHESS TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

def main():

    file_name = '/local/dataraid/databank/CHESS/scan1/scan1_.tiff'
    dark_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_dark_.tiff'
    white_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_white_.tiff'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/CHESS.h5'

    sample_name = 'Dummy'

    projections_start = 1
    projections_end = 361
    white_start = 0
    white_end = 1
    white_step = 1
    dark_start = 0
    dark_end = 1
    dark_step = 1

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_digits = 3,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                    )    
    # Save data as dataExchange
    write = dataexchange.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

