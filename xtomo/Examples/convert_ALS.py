# -*- coding: utf-8 -*-
"""
.. module:: convert_ALS.py
   :platform: Unix
   :synopsis: Convert ALS TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read ALS raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import xtomo_importer as xtomo_imp 
import xtomo_exporter as xtomo_exp

import re

def main():

    file_name = '/local/dataraid/databank/templates/als_beamline_8.3.2/sample_name_0000_.tif'
    dark_file_name = '/local/dataraid/databank/templates/als_beamline_8.3.2/sample_namedrk_.tif'
    white_file_name = '/local/dataraid/databank/templates/als_beamline_8.3.2/sample_namebak_.tif'
    log_file = '/local/dataraid/databank/templates/als_beamline_8.3.2/sample_name.sct'
    hdf5_file_name = '/local/dataraid/databank/templates/dataExchange/tmp/ALS.h5'    

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

        if '-num_bright_field' in line:
            WhiteEnd = re.findall(r'\d+', line)

        if '-num_dark_fields' in line:
            DarkEnd = re.findall(r'\d+', line)

    file.close()
    
    dark_start = 0
    dark_end = int(DarkEnd[0])
    dark_step = 1
    white_start = 0
    white_end = int(WhiteEnd[0])
    white_step = 1
    projections_start = 0
    projections_end = int(Angles[0])
    #projections_end = 18

    print dark_end, white_end, projections_end

    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name = file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 4,
                                                       #data_type='tiff',
                                                       log='INFO'
                                                       )

    # Save data as dataExchange
    write = xtomo_exp.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = Sample,
                          data_exchange_type = 'tomography_raw_projections'
                          )


if __name__ == "__main__":
    main()

