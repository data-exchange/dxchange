# -*- coding: utf-8 -*-
"""
.. module:: main_convert_esrf.py
   :platform: Unix
   :synopsis: Convert SRC dpt files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

#    file_name = '/local/dataraid/databank/SRC/read_data/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_991.268cm-1.dpt'
    file_name = '/local/dataraid/databank/SRC/read_data/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_1700.969cm-1.dpt'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/SRC_2500_50_50_1700.969_01.h5'

    sample_name = 'FPA_16_18_18_TOMO_243_Fiber_2500_50_50_1700.969cm-1'


    
    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
#    slices_start = 100    
#    slices_end = 104    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       sample_name = sample_name,
#                                                       slices_start = slices_start,
#                                                       slices_end = slices_end,
                                                       data_type='dpt',
                                                       log='INFO'
                                                       )

    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

