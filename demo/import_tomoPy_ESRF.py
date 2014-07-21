# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_ESRF.py
   :platform: Unix
   :synopsis: reconstruct ESRF data with TomoPy
   :INPUT
       series of edf files or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx

import re


def main():
    file_name = '/local/dataraid/databank/ESRF/scan.edf'
    dark_file_name = '/local/dataraid/databank/ESRF/dark.edf'
    white_file_name = '/local/dataraid/databank/ESRF/flat.edf'

    # only defined if used a converter
    # omit when used as direct importer in tomoPy    
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/ESRF_test_02.h5'

    sample_name = 'esrf'


    
    # set to import/convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 300    
    slices_end = 304    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       white_file_name = white_file_name,
                                                       dark_file_name = dark_file_name,
                                                       sample_name = sample_name,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       data_type='edf',
                                                       log='INFO'
                                                       )

##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange with:
##    # Read HDF5 file.
##    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
##                                                   slices_start=0,
##                                                   slices_end=2)

    # TomoPy xtomo object creation and pipeline of methods. 
    # for full set of options see http://tomopy.github.io/tomopy/

    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=549.84
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/ESRF_OK', axis=0)

if __name__ == "__main__":
    main()

