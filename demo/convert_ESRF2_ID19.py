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

    source_name = "ESRF"
    beamline = "ID19"
    experimenter_name = "Christopher F. Powell"
    experimenter_affiliation = "Argone National Laboratory"
    experimenter_email = "powell@anl.gov"
    source_mode = "non top-up"

    projections_start = 0
    white_start = 0
    white_step = 1
    dark_start = 0
    dark_end = 1
    dark_step = 1

    sample = 1
    
    if (sample == 1):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/0001_0210675.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0001.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0001_0210675/0001_0210675.info'

    if (sample == 2):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0002_0210675_2nd/0002_0210675_2nd.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0002.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0002_0210675_2nd/0002_0210675_2nd.info'

    if (sample == 3):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/0006_AV67_016_offsetAngleMinus12.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0006.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0006_AV67_016_offsetAngleMinus12/0006_AV67_016_offsetAngleMinus12.info'

    if (sample == 4):
        # white are missing
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/0007_AV67_017_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0007.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0007_AV67_017_offsetAngle0/0007_AV67_017_offsetAngle0.info'

    if (sample == 5):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/0008_AV67_024_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0008.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0008_AV67_024_offsetAngle0/0008_AV67_024_offsetAngle0.info'

    if (sample == 6):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/0009_AV67_018_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0009.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0/0009_AV67_018_offsetAngle0.info'

        # only pre-white, dark are missing
        white_end = 41

    if (sample == 7):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/0009_AV67_018_offsetAngle0_Redo.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0009_Redo.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0009_AV67_018_offsetAngle0_Redo/0009_AV67_018_offsetAngle0_Redo.info'

        # DO NOT CONVERT stopped during data collection 
    ##    file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/0011_AV67_022_offsetAngle0.edf'
    ##    dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/dark.edf'
    ##    white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0011_AV67_022_offsetAngle0/ref.edf'
    ##    hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0011.h5'
    ##    sample_name = '0011_AV67_022_offsetAngle0'
    ##    white_end = 41

    if (sample == 8):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/0012_AV67_022_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0012.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0012_AV67_022_offsetAngle0/0012_AV67_022_offsetAngle0.info'

    if (sample == 9):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/0013_AV67_026_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0013.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0013_AV67_026_offsetAngle0/0013_AV67_026_offsetAngle0.info'

    if (sample == 10):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/0014_AV67_028_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0014.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0014_AV67_028_offsetAngle0/0014_AV67_028_offsetAngle0.info'

    if (sample == 11):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/0015_AV67_020_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0015.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0015_AV67_020_offsetAngle0/0015_AV67_020_offsetAngle0.info'

    if (sample == 12):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/0016_AV67_029_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0016.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0016_AV67_029_offsetAngle0/0016_AV67_029_offsetAngle0.info'

    if (sample == 13):
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/0017_AV67_025_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0017.h5'
        sample_name = '0017_AV67_025_offsetAngle0'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0017_AV67_025_offsetAngle0/0017_AV67_025_offsetAngle0.info'

    if (sample == 14):
        # white are missing
        file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/0018_AV67_011_offsetAngle0.edf'
        dark_file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/dark.edf'
        white_file_name = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/ref.edf'
        hdf5_file_name = '/local/dataraid/databank/dataExchange/ESRF_0018.h5'
        log_file = '/local/dataraid/databank/ESRF_2013Dec/0018_AV67_011_offsetAngle0/0018_AV67_011_offsetAngle0.info'

    #Read ESRF log file data
    file = open(log_file, 'r')
    for line in file:
        linelist=line.split('=')
        if len(linelist)>1:
            if (linelist[0]=="Energy"):
                energy = float(linelist[1])
            elif (linelist[0]=="Prefix"):
                sample_name = linelist[1].lstrip().replace("\n", "")
            elif (linelist[0]=="PixelSize"):
                 actual_pixel_size = float(linelist[1])
            elif (linelist[0]=="Distance"):
                 acquisition_comment = 'Distance sample to detector = ' + linelist[1].lstrip().replace("\n", "") + ' mm'
            elif (linelist[0]=="TOMO_N"):
                 projections_end = int(linelist[1])
            elif (linelist[0]=="REF_N"):
                 white_end = 2 * int(linelist[1])
            elif (linelist[0]=="Date"):
                 source_datetime = linelist[1].lstrip().replace("\n", "")
            elif (linelist[0]=="Scan_Type"):
                 acquisition_mode = linelist[1].lstrip().replace("\n", "")
            elif (linelist[0]=="SrCurrent"):
                 current = float(linelist[1])
            elif (linelist[0]=="Comment"):
                 instrument_comment = linelist[1].lstrip().replace("\n", "")
    file.close()

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
                          data_exchange_type = 'tomography_raw_projections',
                          source_name = source_name,
                          source_mode = source_mode,
                          source_datetime = source_datetime,
                          beamline = beamline,
                          energy = energy,
                          current = current,
                          actual_pixel_size = actual_pixel_size,
                          experimenter_name = experimenter_name,
                          experimenter_affiliation = experimenter_affiliation,
                          experimenter_email = experimenter_email,
                          instrument_comment = instrument_comment,
                          sample_name = sample_name,
                          acquisition_mode = acquisition_mode,
                          acquisition_comment = acquisition_comment,
                          hdf5_file_name = hdf5_file_name,
                          )
    print "energy: ", energy
    print "sample name: ", sample_name
    print "pixel size: ", actual_pixel_size
    print "projections: ", projections_end
    print "whites: ", white_end
    print "experiment date: ", source_datetime
    print "scan mode: ", acquisition_mode
    print "acquitition comment: ", acquisition_comment
    print "current: ", current
    print "instrument comment: ", instrument_comment

if __name__ == "__main__":
    main()

