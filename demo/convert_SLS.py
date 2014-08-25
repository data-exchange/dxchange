# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS_legacy.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read ALS raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re

def main():

##    file_name = '/local/dataraid/databank/SLS_2011/Blakely_SLS/Blakely.tif'
##    log_file = '/local/dataraid/databank/SLS_2011/Blakely_SLS/Blakely.log'
##
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Blakely_SLS_2011.h5'

    file_name = '/local/dataraid/databank/SLS_2011/Hornby_SLS/Hornby_b.tif'
    log_file = '/local/dataraid/databank/SLS_2011/Hornby_SLS/Hornby.log'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Hornby_SLS_2011_01.h5'

    
    #Read SLS log file data
    file = open(log_file, 'r')
    for line in file:
        linelist=line.split()
        if len(linelist)>1:
            if (linelist[0]=="Number" and linelist[2]=="darks"):
                number_of_darks = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="flats"):
                number_of_flats = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="projections"):
                number_of_projections = int(linelist[4])
            elif (linelist[0]=="Rot" and linelist[2]=="min"):
                rotation_min = float(linelist[6])
            elif (linelist[0]=="Rot" and linelist[2]=="max"):
                rotation_max = float(linelist[6])
            elif (linelist[0]=="Angular" and linelist[1]=="step"):
                angular_step = float(linelist[4])
    file.close()

    dark_start = 1
    dark_end = number_of_darks + 1
    white_start = dark_end
    white_end = white_start + number_of_flats
    projections_start = white_end
    projections_end = projections_start + number_of_projections

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 800    
#    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_digits=4,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       log='INFO'
                                                       )
    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )
if __name__ == "__main__":
    main()

