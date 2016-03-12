# -*- coding: utf-8 -*-
"""
.. module:: demo.py
   :platform: Unix
   :synopsis: Generate test files in data exchange.

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

from dxtomo import File, Entry
import numpy as np
import datetime
import os
import time 
def main():

    fname = './demo.h5'

    experimenter_name="Martin Skovgaard Andersen"
    experimenter_affiliation="Technical University of Denmark" 
    experimenter_email="mskan@dtu.dk"
    instrument_comment="Xradia Versa micro CT scanner"  
    sample_name = 'sample_name'


    size  = 180

    scan_index_0 = np.arange(0, size)
    scan_index_0 = [0 for i in scan_index_0]

    scan_index_1 = np.arange(0, size)
    scan_index_1 = [1 for i in scan_index_1]
    print scan_index_0
    print scan_index_1

    scan_index = np.concatenate([scan_index_0, scan_index_1])
    print scan_index

    image_number_0  = np.arange(0, size)
    image_number_1  = np.arange(0, size)
    image_number = np.concatenate([image_number_0, image_number_1])
    print image_number

    time_stamp_0  =  np.arange(0, size*20000000, 20000000)
    time_stamp_1  =  np.arange(0, size*10000000, 10000000)
    time_stamp  = np.concatenate([time_stamp_0, time_stamp_1])
    print time_stamp

    image_exposure_time_0 = np.random.random_integers(10000000, 10005000, size)
    image_exposure_time_1 = np.random.random_integers(20000000, 20005000, size)
    image_exposure_time = np.concatenate([image_exposure_time_0, image_exposure_time_1])
    print image_exposure_time

    image_is_complete_0  = np.ones(size)
    image_is_complete_1  = np.ones(size)
    image_is_complete = np.concatenate([image_is_complete_0, image_is_complete_1])

    print image_is_complete

    today = datetime.datetime.today()
    today = today.isoformat()
    scan_datetime_0 = range(0, size)    scan_datetime_0 = [today for i in scan_datetime_0]

    # Wait for 5 seconds    time.sleep(5)

    today = datetime.datetime.today()
    today = today.isoformat()
    scan_datetime_1 = range(0, size)    scan_datetime_1 = [today for i in scan_datetime_1]

    scan_datetime = np.concatenate([scan_datetime_0, scan_datetime_1])
    print scan_datetime

    image_theta_0 = range(0, 180, 180/size)
    image_theta_1 = range(0, 180, 180/size)
    image_theta = np.concatenate([image_theta_0, image_theta_1])
    
    print image_theta

    if (fname != None):
        if os.path.isfile(fname):
            print "Data Exchange file already exists: ", fname
        else:
            # Create new folder.
            dirPath = os.path.dirname(fname)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            # Write the Data Exchange HDF5 file.
            # Open DataExchange file
            f = File(fname, mode='w') 

            f.add_entry(Entry.experimenter(name={'value':experimenter_name}))
            f.add_entry(Entry.experimenter(affiliation={'value':experimenter_affiliation}))
            f.add_entry(Entry.experimenter(email={'value':experimenter_email}))
            f.add_entry(Entry.instrument(comment={'value': instrument_comment}))
            f.add_entry(Entry.sample( name={'value':sample_name}))
            f.add_entry(Entry.acquisition(scan_index={'value': scan_index}))
            f.add_entry(Entry.acquisition(scan_datetime={'value': scan_datetime}))                
            f.add_entry(Entry.acquisition(image_theta={'value': image_theta, 'units': 'degrees'}))
            f.add_entry(Entry.acquisition(time_stamp={'value':time_stamp, 'units': '1e-7s', 'dataset_opts': {'dtype': 'd'}})) 
            f.add_entry(Entry.acquisition(image_number={'value': image_number}))
            f.add_entry(Entry.acquisition(image_exposure_time={'value':image_exposure_time, 'units': '1e-7s', 'dataset_opts': {'dtype': 'd'}}))
            f.add_entry(Entry.acquisition(image_is_complete={'value': image_is_complete}))

            f.close()
 
    else:
           print "Nothing to do ..."

if __name__ == "__main__":
    main()

