# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_Elettra.py
   :platform: Unix
   :synopsis: reconstruct Elettra Synchrotron Facility data with TomoPy
   :INPUT
       series of tiff or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


def main():

    file_name = '/media/DISK_01/databank/dataExchange/microCT/Elettra.h5'
    file_name_out = '/media/DISK_01/databank/dataExchange/microCT/Elettra_out.h5'

    
#    slices_start = 150    
#    slices_end = 154    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       data_type='h5',
                                                       log='INFO'
                                                       )

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

