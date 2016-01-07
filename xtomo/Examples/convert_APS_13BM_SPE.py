# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_13BM_SPE.py
   :platform: Unix
   :synopsis: Convert APS 13-BM SPE files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 13-BM SPE raw tomographic data and save them as Data Exchange

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

    file_name = '/local/dataraid/databank/templates/aps_13-BM/SPE/sample_name_.SPE'
    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/APS_13_BM_spe.h5'

    white_start = 1
    white_end = 8
    white_step = 2
    projections_start = 2
    projections_end = 7
    projections_step = 2

    sample_name = 'run2_soln1_2'

    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_step = projections_step,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       projections_zeros=False,
                                                       white_zeros=False,
                                                       dark_zeros=False,
                                                       projections_digits = 1,
                                                       data_type='spe',
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

