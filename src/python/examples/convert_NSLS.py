# -*- coding: utf-8 -*-
"""
.. module:: main_convert_NSLS.py
   :platform: Unix
   :synopsis: Convert NSLS TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx
#import tomopy


def main():

##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/rad_0400ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/ff_0350ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_01.h5'
##
##    white_start = 0
##    white_end = 2580
##    white_step = 30
##    projections_start = 0
##    projections_end = 2600
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_02/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_02/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_02.h5'
##
##    white_start = 0
##    white_end = 2580
##    white_step = 30
##    projections_start = 0
##    projections_end = 2600
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##     
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_03/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_03/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_03.h5'
##
##    white_start = 0
##    white_end = 2580
##    white_step = 30
##    projections_start = 0
##    projections_end = 2600
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_05/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_05/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_05.h5'
##
##    white_start = 0
##    white_end = 2580
##    white_step = 30
##    projections_start = 0
##    projections_end = 2600
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )

##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_-08/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_-08/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_01_-08.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )

##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_2/rad_0325ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_2/ff_0275ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_01_2.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )

##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_-36/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_01_-36/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_01_-36.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-08/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-08/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_02_-08.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )

##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_2/rad_0325ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_2/ff_0275ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_02_2.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-36/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-36/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_02_-36.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-54/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_02_-54/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_02_-54.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-08/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-08/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_03_-08.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_2/rad_0325ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_2/ff_0275ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_03_2.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-36/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-36/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_03_-36.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-54/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_3_03_-54/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_3_03_-54.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_02/rad_0400ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_02/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_02.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_03/rad_0300ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_03/ff_0250ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_03.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y25/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y25/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_04_Y25.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )
##
##    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-3/rad_0350ms_.tiff'
##    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-3/ff_0300ms_.tiff'
##
##    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_04_Y-3.h5'
##
##    white_start = 0
##    white_end = 1490
##    white_step = 30
##    projections_start = 0
##    projections_end = 1500
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_file_name = white_file_name,
##                            white_start = white_start,
##                            white_end = white_end,
##                            white_step = white_step,
##                            log='WARNING'
##                            )

    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-31/rad_0400ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-31/ff_0300ms_.tiff'

    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_04_Y-31.h5'

    white_start = 0
    white_end = 1490
    white_step = 30
    projections_start = 0
    projections_end = 1500

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-54/rad_0400ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_4_04_Y-54/ff_0300ms_.tiff'

    hdf5_file_name = '/local/dataraid/dataraid/tmp/92_4_04_Y-54.h5'

    white_start = 0
    white_end = 1490
    white_step = 30
    projections_start = 0
    projections_end = 1500

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_file_name = white_file_name,
                            white_start = white_start,
                            white_end = white_end,
                            white_step = white_step,
                            log='WARNING'
                            )
if __name__ == "__main__":
    main()

