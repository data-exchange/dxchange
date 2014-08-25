# -*- coding: utf-8 -*-
"""
.. module:: convert_Northwestern.py
   :platform: Unix
   :synopsis: Convert SLS TOMCAT TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read SLS TOMCAT TIFF raw tomographic data and save them as Data Exchange

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

    file_name = '/local/dataraid/databank/SLS_2011/Ashley/3e_final_2_.tif'
    log_file = '/local/dataraid/databank/SLS_2011/Ashley/3e_final_2_.log'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Ashley_SLS.h5'

    #Read SLS log file data
    file = open(log_file, 'r')

    for line in file:
        if 'Number of darks' in line:
            NumberOfDarks = re.findall(r'\d+', line)
        if 'Number of flats' in line:
            NumberOfFlats = re.findall(r'\d+', line)
        if 'Number of projections' in line:
            NumberOfProjections = re.findall(r'\d+', line)
        if 'Number of inter-flats' in line:
            NumberOfInterFlats = re.findall(r'\d+', line)
        if 'Inner scan flag' in line:
            InnerScanFlag = re.findall(r'\d+', line)
        if 'Flat frequency' in line:
            FlatFrequency = re.findall(r'\d+', line)
        if 'Rot Y min' in line:
            RotYmin = re.findall(r'\d+.\d+', line)
        if 'Rot Y max' in line:
            RotYmax = re.findall(r'\d+.\d+', line)
        if 'Angular step' in line:
            AngularStep = re.findall(r'\d+.\d+', line)
    file.close()

    dark_start = 1
    dark_end = int(NumberOfDarks[0]) + 1
    white_start = dark_end
    white_end = white_start + int(NumberOfFlats[0])
    projections_start = white_end
    projections_end = projections_start + int(NumberOfProjections[0])

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 800    
#    slices_end = 804    
   
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       projections_digits=4,
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

