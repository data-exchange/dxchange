# -*- coding: utf-8 -*-
"""
.. module:: convert_APS_26ID_XRADIA.py
   :platform: Unix
   :synopsis: Convert APS 26-ID XRADIA files in data exchange.

Example on how to use the `xtomo_raw`_ module to read APS 26-ID XRADIA raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

def main():

    file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1_TomoScript_181imgs_p1s_b1.txrm'
    # white is saturated .... 
    white_file_name = '/local/dataraid/databank/TXM_26_ID/20130731_001_Background_Reference_20imgs_p5s_b1.xrm'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/APS_26_ID_xradia.h5'

    sample_name = '20130731_004_Stripe_Solder_Sample_Tip1'

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       white_file_name = white_file_name,                                                       
                                                       data_type='xradia',
                                                       log='INFO'
                                                    )    

    # Save data as dataExchange
    write = dataexchange.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

