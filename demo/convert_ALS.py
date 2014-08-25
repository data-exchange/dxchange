# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>

""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re


def main():
    
    file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08_0000_.tif'
    dark_file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08drk_.tif'
    white_file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08bak_.tif'
    log_file = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08.sct'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/ALS_20140731.h5'

    verbose = True

    # Read ALS log file data
    file = open(log_file, 'r')
    for line in file:
        if '-scanner' in line:
            Source = re.sub(r'-scanner ', "", line)
            if verbose: print 'Facility', Source
        
        if '-object' in line:
            Sample = re.sub(r'-object ', "", line)
            if verbose: print 'Sample', Sample
            
        if '-senergy' in line:
            Energy = re.findall(r'\d+.\d+', line)
            if verbose: print 'Energy', Energy[0]
            
        if '-scurrent' in line:
            Current = re.findall(r'\d+.\d+', line)
            if verbose: print 'Current', Current[0]

        if '-nangles' in line:
            Angles = re.findall(r'\d+', line)
            if verbose: print 'Angles', Angles[0]

        if '-i0cycle' in line:
            WhiteStep = re.findall(r'\s+\d+', line)
            if verbose: print 'White Step', WhiteStep[0]

        if '-num_bright_field' in line:
            WhiteEnd = re.findall(r'\d+', line)

        if '-num_dark_fields' in line:
            DarkEnd = re.findall(r'\d+', line)

    file.close()
    
    dark_start = 0
    dark_end = int(DarkEnd[0])
    dark_step = 1
    white_start = 0
    white_end = int(WhiteEnd[0])
    white_step = int(WhiteStep[0])
    projections_start = 0
    projections_end = int(Angles[0])

    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    #slices_start = 245    
    #slices_end = 265  

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name = file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 4,
                                                       log='INFO'
                                                       )


    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = '20140731_001306_2477A_x00y08',
                          data_exchange_type = 'tomography_raw_projections'
                          )


if __name__ == "__main__":
    main()

