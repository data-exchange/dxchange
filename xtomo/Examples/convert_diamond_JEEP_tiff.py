# -*- coding: utf-8 -*-
"""
.. module:: convert_Diamond.py
   :platform: Unix
   :synopsis: Convert Diamond TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read SLS TOMCAT TIFF raw tomographic data and save them as Data Exchange

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

import re

def main():

    file_name = '/local/dataraid/databank/templates/diamond_JEEP/tiff/sample_name/im_.tif'
    white_file_name = '/local/dataraid/databank/templates/diamond_JEEP/tiff/sample_name/flat_.tif'

    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/Diamond.h5'

    sample_name = 'waterflow'
    

    white_start = 0
    white_end = 1
    projections_start = 1000
    projections_end = 2440


    #print "Dark", dark_start, dark_end 
    print "White", white_start, white_end 
    print "Projection", projections_start, projections_end

    # Read series of images
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_angle_end = 360,
                                                       projections_digits=6,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       log='INFO'
                                                       )
    write = xtomo_exp.Export()
    # Create minimal data exchange hdf5 file
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          sample_name = sample_name,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )


if __name__ == "__main__":
    main()

