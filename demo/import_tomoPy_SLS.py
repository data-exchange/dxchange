# -*- coding: utf-8 -*-
"""
.. module:: convert_SLS.py
   :platform: Unix
   :synopsis: reconstruct SLS Tomcat data with TomoPy
   :INPUT
       series of tiff and log file or data exchange 

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
import tomopy
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re


def main():
    # read a series of tiff
    file_name = '/local/dataraid/databank/SLS_2011/Hornby_SLS/Hornby_b.tif'
    log_file = '/local/dataraid/databank/SLS_2011/Hornby_SLS/Hornby.log'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/Hornby_SLS_2011_01.h5'

    
    #Read SLS log file data
    file = open(log_file, 'r')
    for line in file:
        linelist=line.split()
        if len(linelist)>1:
            if (linelist[0]=="Number" and linelist[2]=="darks"):
                number_of_darks = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="flats"):
                number_of_flats = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="projections"):
                number_of_projections = int(linelist[4])
            elif (linelist[0]=="Rot" and linelist[2]=="min"):
                rotation_min = float(linelist[6])
            elif (linelist[0]=="Rot" and linelist[2]=="max"):
                rotation_max = float(linelist[6])
            elif (linelist[0]=="Angular" and linelist[1]=="step"):
                angular_step = float(linelist[4])
    file.close()

    dark_start = 1
    dark_end = number_of_darks + 1
    white_start = dark_end
    white_end = white_start + number_of_flats
    projections_start = white_end
    projections_end = projections_start + number_of_projections

    # to reconstruct a subset of slices set slices_start and slices_end
    # if omitted the full data set is recontructed
    
    slices_start = 800    
    slices_end = 804    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       log='INFO'
                                                       )

##    # if you have already created a data exchange file using convert_SLS.py module,
##    # comment the call above and read the data set as data exchange 
##    # Read HDF5 file.
##    data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
##                                                   slices_start=0,
##                                                   slices_end=2)

    # TomoPy xtomo object creation and pipeline of methods.  
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    d.normalize()
    d.correct_drift()
    #d.optimize_center()
    #d.phase_retrieval()
    #d.correct_drift()
    d.center=1010.0
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/SLS_', axis=0)

if __name__ == "__main__":
    main()

