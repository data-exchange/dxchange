# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_1ID.py
   :platform: Unix
   :synopsis: Convert APS 1-ID TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 1-ID TIFF raw tomographic data and save them as Data Exchange

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

    file_name = '/local/dataraid/databank/templates/aps_1-ID/data_.tif'
    log_file = '/local/dataraid/databank/templates/aps_1-ID/TomoStillScan.dat'
    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/APS_1_ID.h5'

    #Read APS 1-ID log file data
    file = open(log_file, 'r')
    for line in file:
        linelist=line.split()
        if len(linelist)>1:
            if (linelist[0]=="First" and linelist[1]=="image"):
                projections_start = int(linelist[4])
            elif (linelist[0]=="Last" and linelist[1]=="image"):
                projections_end = int(linelist[4])
            elif (linelist[0]=="Dark" and linelist[1]=="field"):
                dark_start = int(linelist[6])
            elif (linelist[0]=="Number" and linelist[2]=="dark"):
                number_of_dark = int(linelist[5])
            elif (linelist[0]=="White" and linelist[1]=="field"):
                white_start = int(linelist[6])
            elif (linelist[0]=="Number" and linelist[2]=="white"):
                number_of_white = int(linelist[5])
    file.close()
    
    dark_end = dark_start + number_of_dark
    white_end = white_start + number_of_white

    # to fix a data collection looging bug ? 
    white_start = white_start + 1
    dark_start = dark_start +1
    projections_start = projections_start + 11
    projections_end = projections_end - 9
    
    
##    # these are correct per Peter discussion
##    projections_start = 943
##    projections_end = 1853
##    white_start = 1844
##    white_end = 1853
##    dark_start = 1854
##    dark_end = 1863
   
    sample_name = 'CAT4B_2'

    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 6,
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

