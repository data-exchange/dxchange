# -*- coding: utf-8 -*-
"""
.. module:: convert_Australian.py
   :platform: Unix
   :synopsis: Convert Australian Synchrotron Facility TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read Australian Synchrotron Facility TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import xtomo_importer as xtomo_imp 
import xtomo_exporter as xtomo_exp

def main():

    file_name = '/local/dataraid/databank/templates/australian_micro-tomography/SAMPLE_T_.tif'
    dark_file_name = '/local/dataraid/databank/templates/australian_micro-tomography/DF__BEFORE_.tif'
    white_file_name = '/local/dataraid/databank/templates/australian_micro-tomography/BG__BEFORE_.tif'
    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/Australian.h5'

    sample_name = 'Teeth'

    projections_start = 0
    projections_end = 1801
    white_start = 0
    white_end = 10
    white_step = 1
    dark_start = 0
    dark_end = 10
    dark_step = 1

    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       projections_digits = 4,
                                                       white_digits = 2,
                                                       dark_digits = 2,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                    )    
    # Save data as dataExchange
    write = xtomo_exp.Export()
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

