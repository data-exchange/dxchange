# -*- coding: utf-8 -*-
"""
.. module:: convert_DataExchange.py
   :platform: Unix
   :synopsis: Convert APS Data Exchange HDF5 files in data exchange ....

Example on how to use the `series_of_images`_ module to read APS Data Exchange raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Example

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


def main():

    file_name = '/local/dataraid/databank/dataExchange/microCT/Elettra.h5'
    file_name_out = 'tmp/projection_'
    
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name, data_type='h5', projections_start=0, projections_end=16)

    # Save data
    mydata = ex.Export()
    mydata.xtomo_tiff(data = data, output_file = file_name_out, axis=0)

    
    file_name = '/local/dataraid/databank/dataExchange/microCT/Elettra.h5'
    file_name_out = 'tmp/sinogram_'
    
    # Load data
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name, data_type='h5', slices_start=0, slices_end=16)

    # Save data
    mydata = ex.Export()
    mydata.xtomo_tiff(data = data, output_file = file_name_out, axis=1)

if __name__ == "__main__":
    main()

