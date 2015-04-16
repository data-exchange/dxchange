# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_2BM.py
   :platform: Unix
   :synopsis: Convert APS 2-BM HDF4 files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 2-BM HDF4 raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

from pyhdf import SD
import os

def main():

    log_file = '/media/DISK_02/databank/templates/aps_2-BM/Sam01_exp.hdf'
    hdf5_file_name = '/media/DISK_02/databank/templates/dataExchange/tmp/APS_2_BM_hdf4.h5'

    #Read APS 2-BM log file data
    f = SD.SD(log_file)

    sds = f.select('base_name')
    data = sds.get()
    base_name = ''.join(data)
    print base_name

    file_name = os.path.split(log_file)[0] + "/" + "raw" + "/" + base_name + "_.hdf"
     
    sds = f.select('start_angle')
    start_angle = sds.get()[0]

    sds = f.select('end_angle')
    end_angle = sds.get()[0]

    sds = f.select('angle_interval')
    angle_interval = sds.get()[0]

    sds = f.select('num_dark_fields')
    num_dark_fields = sds.get()[0]

    f.end()
    
    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = projections_start + (int)((end_angle -  start_angle) / angle_interval) + 1
    dark_start = projections_end + 1 
    dark_end = dark_start + num_dark_fields

    sample_name = base_name

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                     projections_start = projections_start,
                                                     projections_end = projections_end,
                                                     white_start = white_start,
                                                     white_end = white_end,
                                                     dark_start = dark_start,
                                                     dark_end = dark_end,
                                                     projections_digits = 5,
                                                     data_type = 'hdf4',
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

