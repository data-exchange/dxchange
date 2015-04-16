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

def main():

    file_name = '/media/DISK_02/databank/templates/xradia_dtu/sample_name.txrm'
    hdf5_file_name = '/media/DISK_02/databank/templates/dataExchange/tmp/DTU.h5'
    sample_name = 'halvmaane_150kV-HE6-20X-60s'

    experimenter_name="Martin Skovgaard Andersen"
    experimenter_affiliation="Technical University of Denmark" 
    experimenter_email="mskan@dtu.dk"
    instrument_comment="Xradia Versa micro CT scanner"  

    # Read raw data
    read = dataexchange.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
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

