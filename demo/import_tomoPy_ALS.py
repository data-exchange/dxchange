# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_ALS.py
   :platform: Unix
   :synopsis: Import ALS TIFF files in data exchange.

Example on how to use the `series_of_images`_ module to read ALS raw tomographic data and reconstruct using tomoPy

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

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08_0000_.tif'
    dark_file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08drk_.tif'
    white_file_name = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08bak_.tif'
    log_file = '/local/dataraid/databank/als/data/raw/sacarroll/20140731_001306_2477A_x00y08/20140731_001306_2477A_x00y08.sct'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/ALS.h5'

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
    slices_start = 245    
    slices_end = 249  

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name = file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 4,
                                                       log='INFO'
                                                       )

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=1282.5
    d.gridrec()

    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/ALS_', axis=0)

if __name__ == "__main__":
    main()

