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

    base_name = "/local/dataraid/databank/SRC/read_data/FPA_16_18_18_TOMO_243_Fiber_2500_50_50_"    
    
    log_file = base_name + "wavelength.dpt"
    angle_file = base_name + "angle.dpt"

    # Determine projection angle end    
    file = open(angle_file, 'r')
    lines = file.readlines()
    projections_angle_end = float(lines[0]) + float(lines[1])
    file.close()

    file = open(log_file, 'r')
    for line in file:
        linelist = line.split(",")

        file_name = base_name+linelist[0]+"cm-1.dpt"
        hdf5_file_name = base_name+linelist[0]+"cm-1.h5"
        sample_name = base_name+linelist[0]+"cm-1"

        mydata = dx.Import()
        # Read series of images from a single dpt file
        data, white, dark, theta = mydata.series_of_images(file_name,
                                                        data_type='dpt',
                                                        projections_angle_end = projections_angle_end,
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
    file.close()

if __name__ == "__main__":
    main()

