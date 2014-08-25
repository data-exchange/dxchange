# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_1ID.py
   :platform: Unix
   :synopsis: Convert APS 1-ID TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read APS 1-ID TIFF raw tomographic data and save them as Data Exchange

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

    file_name = '/local/dataraid/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_.tif'
    log_file = '/local/dataraid/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_TomoStillScan.dat'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/APS_01ID.h5'

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
   
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 1000    
#    slices_end = 1004    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 6,
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

