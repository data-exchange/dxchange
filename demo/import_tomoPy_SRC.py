# -*- coding: utf-8 -*-
"""
.. module:: import_tomoPy_SRC.py
   :platform: Unix
   :synopsis: Import Synchrotron Radiation Center DPT files in data exchange.

Example on how to use the `series_of_images`_ module to read Synchrotron Radiation Center Infrared raw tomographic data and reconstruct with tomoPy

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

# tomoPy: https://github.com/tomopy/tomopy
import tomopy 

# Data Exchange: https://github.com/data-exchange/data-exchange
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

import re
import os

def main():
    # only used to locate the wavelenght.dpt and angle.dpt files   
    raw_tiff_base_name = "/local/dataraid/databank/dataExchange/microCT/SRC/raw/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_"    
    
    hdf5_base_name = "/local/dataraid/databank/dataExchange/microCT/SRC/dx/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_"    
    
    log_file = raw_tiff_base_name + "wavelength.dpt"
    angle_file = raw_tiff_base_name + "angle.dpt"
    
    dir_name = os.path.dirname(hdf5_base_name)
    sample_name_prefix = os.path.basename(hdf5_base_name)
    
    print dir_name
    print sample_name_prefix

    file = open(log_file, 'r')
    for line in file:
        linelist=line.split(",")

        hdf5_file_name = hdf5_base_name+linelist[0]+"cm-1.h5"
        sample_name = hdf5_base_name+linelist[0]+"cm-1"
    
        # set to read slices between slices_start and slices_end
        # if omitted all data set will be converted   
        slices_start = 30    
        slices_end = 36    

        # to create a data exchange file use convert_SRC.py module,
        data, white, dark, theta = tomopy.xtomo_reader(hdf5_file_name,
                                                    slices_start=slices_start,
                                                    slices_end=slices_end)

        # TomoPy xtomo object creation and pipeline of methods.  
        d = tomopy.xtomo_dataset(log='debug')
        d.dataset(data, white, dark, theta)
        d.normalize()
        d.correct_drift()
        #d.optimize_center()
        #d.phase_retrieval()
        #d.correct_drift()
        d.center=64
        d.gridrec()

        # Write to stack of TIFFs.
        rec_name = dir_name + "/rec/" + sample_name_prefix + linelist[0] + "cm-1"

        # Write to stack of TIFFs.
        mydata = ex.Export()
        mydata.xtomo_tiff(data = d.data_recon, output_file = rec_name, axis=0)

    file.close()

if __name__ == "__main__":
    main()

