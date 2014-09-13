# -*- coding: utf-8 -*-
"""
.. module:: convert_DataExchange.py
   :platform: Unix
   :synopsis: Convert APS Data Exchange HDF5 files in data exchange ....

Example on how to use the `xtomo_raw`_ module to read APS Data Exchange raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


def main():

    file_name = '/local/dataraid/databank/dataExchange/microCT/Elettra.h5'
    file_name_out = '/local/dataraid/databank/dataExchange/microCT/Elettra_out.h5'

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name, data_type='h5', log='INFO')

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = file_name_out,
                          data_exchange_type = 'tomography_raw_projections')

if __name__ == "__main__":
    main()

