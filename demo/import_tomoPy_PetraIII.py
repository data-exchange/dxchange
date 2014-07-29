# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_PetraIII.py
   :platform: Unix
   :synopsis: reconstruct PetraIII P06 beamline data with TomoPy
   :INPUT
       series of tiff or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx


def main():
    # read a series of tiff

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 0 -> 19
    file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0002/ccd/pco01/ccd_.tif'
    dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0000/ccd/pco01/ccd_.tif'
    white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0001/ccd/pco01/ccd_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII_oster02_0000.h5'
    sample_name = 'PetraIII P06 oster02_0000'

    projections_start = 0
    projections_end = 1441
    white_start = 0
    white_end = 20
    white_step = 1
    dark_start = 0
    dark_end = 20
    dark_step = 1

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 0 -> 19
    file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0002/ccd/pco01/ccd_.tif'
    dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0000/ccd/pco01/ccd_.tif'
    white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0001/ccd/pco01/ccd_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII_oster02_0001.h5'
    sample_name = 'PetraIII P06 oster02_0001'

    projections_start = 0
    projections_end = 1441
    white_start = 0
    white_end = 20
    white_step = 1
    dark_start = 0
    dark_end = 20
    dark_step = 1

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 3 -> 19
    file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0002/ccd/pco01/ccd_.tif'
    dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0000/ccd/pco01/ccd_.tif'
    white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0001/ccd/pco01/ccd_.tif'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII_oster02_0002.h5'
    sample_name = 'PetraIII P06 oster02_0002'

    projections_start = 0
    projections_end = 1441
    white_start = 0
    white_end = 20
    white_step = 1
    dark_start = 3
    dark_end = 20
    dark_step = 1

    # to reconstruct slices from slices_start to slices_end
    # if omitted all data set is recontructed
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       #projections_angle_range=360,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       sample_name = sample_name,
                                                       projections_digits = 4,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                       )


##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
##    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
##                                                   slices_start=slice_start,
##                                                   slices_end=slice_end)

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    d.phase_retrieval()
    #d.correct_drift()
    d.center=1870.921875
    d.gridrec()


    # Write to stack of TIFFs.
#    tomopy.xtomo_writer(d.data_recon, 'tmp/oster02_0000_', axis=0)
#    tomopy.xtomo_writer(d.data_recon, 'tmp/oster02_0001_', axis=0)
    tomopy.xtomo_writer(d.data_recon, 'tmp/oster02_0002_', axis=0)

if __name__ == "__main__":
    main()

