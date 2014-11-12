# -*- coding: utf-8 -*-
"""
.. module:: convert_ESRF.py
   :platform: Unix
   :synopsis: Convert ESRF edf files in data exchange.

Example on how to use the `xtomo_raw`_ module to read ESRF edf raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/ESRF2/0006_AV67_016_offsetAngleMinus12/0006_AV67_016_offsetAngleMinus12.edf'
    #dark_file_name = '/local/dataraid/databank/ESRF2/0006_AV67_016_offsetAngleMinus12/dark2_.edf'
    white_file_name = '/local/dataraid/databank/ESRF2/0006_AV67_016_offsetAngleMinus12/ref.edf'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/ESRF2.h5'

    sample_name = '0006_AV67_016_offsetAngleMinus12'

    projections_start = 0
    projections_end = 2003
    white_start = 0
    white_end = 40
    white_step = 1
#    dark_start = 0
#    dark_end = 10
#    dark_step = 1

    
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 300    
#    slices_end = 304    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
#                                                       dark_file_name = dark_file_name,
#                                                       dark_start = dark_start,
#                                                       dark_end = dark_end,
#                                                       dark_step = dark_step,
                                                       projections_digits = 4,
                                                       white_digits = 4,
#                                                       dark_digits = 4,
                                                       projections_zeros = True,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       data_type='edf2',
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

