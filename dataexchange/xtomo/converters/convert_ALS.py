# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>

""" 

import xtomo.xtomo_importer as dx

import re


def main():
    
    file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS_.tif'
    dark_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSdrk_.tif'
    white_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSbak_.tif'
    log_file = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS.sct'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/blakely_ALS_2011_01.h5'

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

    file.close()

    dark_start = 0
    dark_end = 20
    dark_step = 1
    white_start = 0
    white_end = int(Angles[0]) 
    white_step = int(WhiteStep[0])
    projections_start = 0
    projections_end = int(Angles[0])

    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name = file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            dark_file_name = dark_file_name,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            dark_step = dark_step,
                            projections_zeros = False,
                            white_zeros = False,
                            dark_zeros = False,
                            log='INFO'
                            )

if __name__ == "__main__":
    main()

