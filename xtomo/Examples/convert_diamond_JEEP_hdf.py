# -*- coding: utf-8 -*-
"""
.. module:: convert_Diamond.py
   :platform: Unix
   :synopsis: Convert Diamond NeXuS files in data exchange.

Example on how to use the `xtomo_raw`_ module to read Diamond NeXuS raw tomographic data and save them as Data Exchange

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

def main():

    file_name = '/local/dataraid/databank/templates/diamond_JEEP/sample_name_subx.nxs'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Diamond.h5'

    # Read raw data 
    # set slice_start and slice_end to  full size. 1600-1610 is for testing only
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name, 
                                                        data_type='nxs', 
                                                        slices_start=1600,
                                                        slices_end=1610,
                                                        slices_step=1,
                                                        log='INFO')
    
    
    # Save data as dataExchange
    write = xtomo_exp.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections')

if __name__ == "__main__":
    main()

