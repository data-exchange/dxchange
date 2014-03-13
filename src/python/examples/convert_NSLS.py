# -*- coding: utf-8 -*-
"""
.. module:: main_convert_NSLS.py
   :platform: Unix
   :synopsis: Convert NSLS TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx
#import tomopy

## NOT CHECKED

def main():

    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/rad_0400ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_01/ff_0350ms_.tiff'

    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_01.h5'

    white_start = 0
    white_end = 2580
    white_step = 30
    projections_start = 0
    projections_end = 2600

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

    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_02/rad_0300ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_02/ff_0250ms_.tiff'

    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_02.h5'

    white_start = 0
    white_end = 2580
    white_step = 30
    projections_start = 0
    projections_end = 2600

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
     
    file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_03/rad_0300ms_.tiff'
    white_file_name = '/local/dataraid/2013_11/Vincent_201311/GA_exp/92_2_03/ff_0250ms_.tiff'

    hdf5_file_name = '/local/dataraid/dataraid/tmp/GA_92_2_03.h5'

    white_start = 0
    white_end = 2580
    white_step = 30
    projections_start = 0
    projections_end = 2600

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

