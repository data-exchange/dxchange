"""
.. module:: convert_APS_13BM.py
   :platform: Unix
   :synopsis: Convert APS 13-BM netCDF files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/APS_13_BM/NC/Dorthe_F_.nc'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/xx_APS_13_BM_NC.h5'

    white_start = 1
    white_end = 4
    white_step = 2
    projections_start = 2
    projections_end = 3
    projections_step = 1

    mydata = dx.Import()
    
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       hdf5_file_name = hdf5_file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_step = projections_step,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       projections_digits = 3,
                                                       data_type='nc',
                                                       sample_name = 'Stripe_Solder_Sample_Tip1',
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
