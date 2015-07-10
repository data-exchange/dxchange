# -*- coding: utf-8 -*-
"""
.. module:: convert_SLS.py
   :platform: Unix
   :synopsis: Convert SLS TOMCAT TIFF files in data exchange.

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

    file_name = '/local/dataraid/databank/templates/sls_tomcat/sample_name.tif'
    log_file = '/local/dataraid/databank/templates/sls_tomcat/sample_name.log'
    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/SLS.h5'

    sample_name = 'Hornby_b'
    
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
    projections_angle_end = 180 + angular_step

    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_angle_end = projections_angle_end,
                                                       projections_digits=4,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
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

