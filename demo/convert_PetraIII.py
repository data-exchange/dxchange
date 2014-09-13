# -*- coding: utf-8 -*-
"""
.. module:: convert_PetraIII.py
   :platform: Unix
   :synopsis: Convert Petra III P05 and P06 TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read  Petra III P05 and P06 TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():


    # Petra III collects data over 360deg but in this data sets they had problem with the rotary
    # stage stop moving . This happened after 180 deg so picking the first 180 deg are good to reconstruct.
    # The 3 blocks below load only the good 180 deg

    ### ct2: pj: from 0 -> 3600; bf from 0 -> 20; df from 0 -> 20
    ##file_name = '/local/data/databank/PetraIII/ct2/ct2_.tif'
    ##dark_file_name = '/local/data/databank/PetraIII/ct2/df2b_.tif'
    ##white_file_name = '/local/data/databank/PetraIII/ct2/bf2b_.tif'
    ##hdf5_file_name = '/local/data/databank/dataExchange/microCT/PetraIII_ct2_180.h5'
    ##sample_name = 'ct2'
    ##
    ### ct2: Wheat root
    ### Sample measured at room temperature
    ##
    ##projections_start = 0
    ##projections_end = 1801
    ##white_start = 0
    ##white_end = 20
    ##white_step = 1
    ##dark_start = 0
    ##dark_end = 20
    ##dark_step = 1

    ### ct3: pj: from 0 -> 3601; bf from 20 -> 39; df from 0 -> 19
    ##file_name = '/local/data/databank/PetraIII/ct3/ct3_.tif'
    ##dark_file_name = '/local/data/databank/PetraIII/ct3/df_.tif'
    ##white_file_name = '/local/data/databank/PetraIII/ct3/bf_.tif'
    ##hdf5_file_name = '/local/data/databank/dataExchange/microCT/PetraIII_ct3_180.h5'
    ##sample_name = 'ct3'
    ##
    ### ct3: Wheat root
    ### Same sample as ct3 but measured at cryogenic condition
    ##
    ##projections_start = 0
    ##projections_end = 1801
    ##white_start = 20
    ##white_end = 40
    ##white_step = 1
    ##dark_start = 0
    ##dark_end = 20
    ##dark_step = 1

    ## ct4: pj: from 0 -> 1199; bf from 1 -> 18; df from 0 -> 19
    #file_name = '/local/dataraid/databank/PetraIII/ct4/ct4_.tif'
    #dark_file_name = '/local/dataraid/databank/PetraIII/ct4/df_ct4_.tif'
    #white_file_name = '/local/dataraid/databank/PetraIII/ct4/bf_ct4_.tif'
    #hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII_ct4_180.h5'
    #sample_name = 'ct4'

    ## ct4: Leaf of rice
    ## Fresh sample measured at cryogenic condition

    #projections_start = 0
    #projections_end = 601
    #white_start = 1
    #white_end = 19
    #white_step = 1
    #dark_start = 0
    #dark_end = 20
    #dark_step = 1

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 3 -> 19
    #file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0002/ccd/pco01/ccd_.tif'
    #dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0000/ccd/pco01/ccd_.tif'
    #white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0002/scan_0001/ccd/pco01/ccd_.tif'
    #hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII_oster02_0002.h5'

    #projections_start = 0
    #projections_end = 1441
    #white_start = 0
    #white_end = 20
    #white_step = 1
    #dark_start = 3
    #dark_end = 20
    #dark_step = 1

    #sample_name = 'PetraIII P06 oster02_0002'

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 0 -> 19
    #file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0002/ccd/pco01/ccd_.tif'
    #dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0000/ccd/pco01/ccd_.tif'
    #white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0000/scan_0001/ccd/pco01/ccd_.tif'
    #hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/PetraIII.h5'

    #projections_start = 0
    #projections_end = 1441
    #white_start = 0
    #white_end = 20
    #white_step = 1
    #dark_start = 0
    #dark_end = 20
    #dark_step = 1

    #sample_name = 'PetraIII P06 oster02_0000'

    # oster: pj: from 0 -> 1440; bf from 0 -> 19; df from 0 -> 19
    file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0002/ccd/pco01/ccd_.tif'
    dark_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0000/ccd/pco01/ccd_.tif'
    white_file_name = '/local/dataraid/databank/PetraIII/2011_KW16_oster/oster02_0001/scan_0001/ccd/pco01/ccd_.tif'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/PetraIII.h5'

    projections_start = 0
    projections_end = 1441
    white_start = 0
    white_end = 20
    white_step = 1
    dark_start = 0
    dark_end = 20
    dark_step = 1

    sample_name = 'PetraIII P06 oster02_0001'
    
    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       #projections_angle_range=360,
                                                       white_file_name = white_file_name,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       white_step = white_step,
                                                       dark_file_name = dark_file_name,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       dark_step = dark_step,
                                                       projections_digits = 4,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                       )
    mydata = ex.Export()
    # Create minimal data exchange hdf5 file
    mydata.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )
if __name__ == "__main__":
    main()

