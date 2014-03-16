# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_2BM.py
   :platform: Unix
   :synopsis: Convert APS 2-BM HDF4 files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import data_exchange as dx

def main():

##    file_name = '/local/dataraid/databank/APS_2_BM/Sam18_hornby/raw/Hornby_19keV_10x_.hdf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Hornby_19keV_10x_APS_2011_01.h5'
##
##    white_start = 1
##    white_end = 2
##    projections_start = 2
##    projections_end = 1503
##    dark_start = 1504
##    dark_end = 1505
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_start = white_start,
##                            white_end = white_end,
##                            dark_start = dark_start,
##                            dark_end = dark_end,
##                            projections_digits = 5,
##                            data_type = 'hdf4',
##                            log='WARNING'
##                            )

##    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam01/raw/TAO_5x_.hdf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam01_TAO_5x.h5'
##
##    white_start = 1
##    white_end = 2
##    projections_start = 2
##    projections_end = 1503
##    dark_start = 1504
##    dark_end = 1505
##
##    mydata = dx.Convert()
##    # Create minimal hdf5 file
##    mydata.series_of_images(file_name,
##                            hdf5_file_name = hdf5_file_name,
##                            projections_start = projections_start,
##                            projections_end = projections_end,
##                            white_start = white_start,
##                            white_end = white_end,
##                            dark_start = dark_start,
##                            dark_end = dark_end,
##                            projections_digits = 5,
##                            data_type = 'hdf4',
##                            log='WARNING'
##                            )



    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam02/raw/TAO_5x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam02_TAO_5x.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam03/raw/TAO_4x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam03_TAO_4x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam04/raw/TAO_4x_200mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam04_TAO_4x_200mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam05/raw/TAO_2.5x_200mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam05_TAO_2.5x_200mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam06/raw/TAO_2.5x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam06_TAO_2.5x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample1/Sam06/raw/TAO_2.5x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample1_Sam06_TAO_2.5x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam01/raw/TAO_2.5x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam01_TAO_2.5x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam02/raw/TAO_2.5x_200mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam02_TAO_2.5x_200mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam03/raw/TAO_4x_200mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam03_TAO_4x_200mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam04/raw/TAO_4x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam04_TAO_4x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam05/raw/TAO_5x_30mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam05_TAO_5x_30mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

    file_name = '/local/dataraid/2014_03/Francesco/Sample2/Sam06/raw/TAO_5x_200mm_.hdf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/multiscale/2BM/Sample2_Sam06_TAO_5x_200mm.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = dx.Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            projections_digits = 5,
                            data_type = 'hdf4',
                            log='WARNING'
                            )

if __name__ == "__main__":
    main()

