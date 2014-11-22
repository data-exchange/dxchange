# -*- coding: utf-8 -*-
"""
.. module:: convert_ESRF2.py
   :platform: Unix
   :synopsis: Convert ESRF edf files in data exchange.

Example on how to use the `xtomo_raw`_ module to read a series of ESRF edf raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.11.12

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    projections_start = 0
    projections_end = 2000
    white_start = 0
    white_end = 82
    white_step = 1
    dark_start = 0
    dark_end = 1
    dark_step = 1

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/0001_0210675.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0001.h5'
##    sample_name = '0001_0210675'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0002_0210675_2nd/0002_0210675_2nd.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0002.h5'
##    sample_name = '0002_0210675_2nd'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/0006_AV67_016_offsetAngleMinus12.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0006.h5'
##    sample_name = '0006_AV67_016_offsetAngleMinus12'

    # white are missing
#    file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/0007_AV67_017_offsetAngle0.edf'
#    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/dark.edf'
#    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/ref.edf'
#    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0007.h5'
#    sample_name = '0007_AV67_017_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/0008_AV67_024_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0008.h5'
##    sample_name = '0008_AV67_024_offsetAngle0'

    # dark are missing, only pre-white
##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/0009_AV67_018_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0009.h5'
##    sample_name = '0009_AV67_018_offsetAngle0'
##    white_end = 41

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/0009_AV67_018_offsetAngle0_Redo.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0009_Redo.h5'
##    sample_name = '0009_AV67_018_offsetAngle0_Redo'

    # DO NOT CONVERT stopped during data collection 
##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/0011_AV67_022_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0011.h5'
##    sample_name = '0011_AV67_022_offsetAngle0'
##    white_end = 41

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/0012_AV67_022_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0012.h5'
##    sample_name = '0012_AV67_022_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/0013_AV67_026_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0013.h5'
##    sample_name = '0013_AV67_026_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/0014_AV67_028_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0014.h5'
##    sample_name = '0014_AV67_028_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/0015_AV67_020_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0015.h5'
##    sample_name = '0015_AV67_020_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/0016_AV67_029_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0016.h5'
##    sample_name = '0016_AV67_029_offsetAngle0'

##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/0017_AV67_025_offsetAngle0.edf'
##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/dark.edf'
##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/ref.edf'
##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0017.h5'
##    sample_name = '0017_AV67_025_offsetAngle0'

    # white are missing
    file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/0018_AV67_011_offsetAngle0.edf'
    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/dark.edf'
    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/ref.edf'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0018.h5'
    sample_name = '0018_AV67_011_offsetAngle0'

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
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
                                                       projections_digits = 4,
                                                       white_digits = 4,
                                                       dark_digits = 4,
                                                       projections_zeros = True,
                                                       data_type='edf2',
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

