# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_ALS.py
   :platform: Unix
   :synopsis: reconstruct ALS tiff data with TomoPy
   :INPUT
       series of tiff and sct file or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    # read a series of tiff
    file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS_.tif'
    dark_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSdrk_.tif'
    white_file_name = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALSbak_.tif'
    log_file = '/local/dataraid/databank/ALS_2011/Blakely/blakely_raw/blakelyALS.sct'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/blakely_ALS_2011_test.h5'

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

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    
    slices_start = 800    
    slices_end = 804    

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

##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
##    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
##                                                   slices_start=0,
##                                                   slices_end=2)

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=1683.8
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/ALS_', axis=0)

if __name__ == "__main__":
    main()

