# -*- coding: utf-8 -*-
"""
.. module:: convert_xradia.py
   :platform: Unix
   :synopsis: Convert xradia files in data exchange.

Example on how to use the `xtomo_raw`_ module to read xradia raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange

import dataexchange.xtomo.formats.xradia_xrm as xradia
import dataexchange.xtomo.formats.data_struct as dstruct

def main():

    #file_name = '/local/dataraid/databank/TXM_26_ID/20130731_004_Stripe_Solder_Sample_Tip1_TomoScript_181imgs_p1s_b1.txrm'
    # white is saturated .... 
    #white_file_name = '/local/dataraid/databank/TXM_26_ID/20130731_001_Background_Reference_20imgs_p5s_b1.xrm'
    #hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/xradia_033.h5'
    #sample_name = '20130731_004_Stripe_Solder_Sample_Tip1'

    file_name = '/local/dataraid/databank/DTU_Imaging_Center/halvmaane_150kV-HE6-20X-60s.txrm'
    hdf5_file_name = '/local/dataraid/databank/dataExchange/Lorentz/dtu/DTU_02.h5'
    sample_name = 'halvmaane_150kV-HE6-20X-60s'

    experimenter_name="Martin Skovgaard Andersen"
    experimenter_affiliation="Technical University of Denmark" 
    experimenter_email="mskan@dtu.dk"
    instrument_comment="Xradia Versa micro CT scanner"  

    # Read data from file.
    reader = xradia.xrm()
    array = dstruct
    reader.read_txrm(file_name, array)

    print "axes", array.exchange.data_axes
    print "energy:", array.exchange.energy[0]
    print "energy units:",  array.exchange.energy_units
    print "angles:", array.exchange.angles
    print "exposure time:", array.spectromicroscopy.data_dwell[0]


    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       #white_file_name = white_file_name,                                                       
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
                          experimenter_name=experimenter_name, 
                          experimenter_affiliation=experimenter_affiliation, 
                          experimenter_email=experimenter_email, 
                          instrument_comment=instrument_comment,  
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()

