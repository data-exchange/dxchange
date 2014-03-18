# -*- coding: utf-8 -*-
"""
.. module:: convert_SLS.py
   :platform: Unix
   :synopsis: Convert SLS Tomcat TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import xtomo.xtomo_importer as dx

import re

def main():

    file_name = '/local/dataraid/databank/SLS_2011/Blakely_SLS/Blakely.tif'
    log_file = '/local/dataraid/databank/SLS_2011/Blakely_SLS/Blakely.log'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Blakely_SLS_2011_01.h5'

    #Read SLS log file data
    file = open(log_file, 'r')

    for line in file:
        if 'Number of darks' in line:
            NumberOfDarks = re.findall(r'\d+', line)
        if 'Number of flats' in line:
            NumberOfFlats = re.findall(r'\d+', line)
        if 'Number of projections' in line:
            NumberOfProjections = re.findall(r'\d+', line)
        if 'Number of inter-flats' in line:
            NumberOfInterFlats = re.findall(r'\d+', line)
        if 'Inner scan flag' in line:
            InnerScanFlag = re.findall(r'\d+', line)
        if 'Flat frequency' in line:
            FlatFrequency = re.findall(r'\d+', line)
        if 'Rot Y min' in line:
            RotYmin = re.findall(r'\d+.\d+', line)
        if 'Rot Y max' in line:
            RotYmax = re.findall(r'\d+.\d+', line)
        if 'Angular step' in line:
            AngularStep = re.findall(r'\d+.\d+', line)
    file.close()

    dark_start = 1
    dark_end = int(NumberOfDarks[0]) + 1
    white_start = dark_end
    white_end = white_start + int(NumberOfFlats[0])
    projections_start = white_end
    projections_end = projections_start + int(NumberOfProjections[0])

    mydata = dx.Import()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                            #hdf5_file_name = hdf5_file_name,
                            projections_start = projections_start,
                            projections_end = projections_end,
                            white_start = white_start,
                            white_end = white_end,
                            dark_start = dark_start,
                            dark_end = dark_end,
                            log='INFO'
                            )

if __name__ == "__main__":
    main()

