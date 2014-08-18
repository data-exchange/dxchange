# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_2BM.py
   :platform: Unix
   :synopsis: Convert APS 2-BM HDF4 files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from pyhdf import SD
import os

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    log_file = '/local/dataraid/databank/Sangid/Sam02/Sam02_exp.hdf'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Sangid_LongFiber.h5'

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
    
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
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
    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          sample_name = sample_name,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

