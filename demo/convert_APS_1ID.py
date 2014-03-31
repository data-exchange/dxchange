# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_1ID.py
   :platform: Unix
   :synopsis: Convert APS 1-ID TIFF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_.tif'
    log_file = '/local/dataraid/databank/APS_1_ID/APS1ID_Cat4B_2/CAT4B_2_TomoStillScan.dat'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/CAT4B_2.h5'

    # to do: add log_file parser
    projections_start = 943
    projections_end = 1853
    white_start = 1844
    white_end = 1853
    dark_start = 1854
    dark_end = 1863
   
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       projections_digits = 6,
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

