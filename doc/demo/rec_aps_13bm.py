#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 13-BM tomography 
data as original netcdf files. To use, change fname to just 
the file name (e.g. 'sample[2].nc' would be 'sample'.
"""
import glob
import numpy as np
import tomopy as tp
import dxchange as dx

from netCDF4 import Dataset

if __name__ == '__main__':
    ## Set path (without file suffix) to the micro-CT data to reconstruct.
    fname = 'data_dir/sample'
    
    ## Create list of data, flat field, and setup files to be read imported.
    files = glob.glob(fname+'*[1-3].nc')
    
    ## Import data.
    proj = dx.exchange.read_aps_13bm(files[1], format = 'netcdf4')
    
    ## Import flat field files.
    flat1 = dx.exchange.read_aps_13bm(files[0], format = 'netcdf4')
    flat2 = dx.exchange.read_aps_13bm(files[2], format = 'netcdf4')
    flat = np.concatenate((flat1, flat2), axis = 0)    
    
    ## Import setup file that has dark.
    setup = glob.glob('*.setup')
    setup = open(setup[0], 'r')
    setup_data = setup.readlines()
    result = {}
    for line in setup_data:
        words = line[:-1].split(':',1)
        result[words[0].lower()] = words[1]

    ## Create array for dark.
    dark = float(result['dark_current'])
    dark = flat*0+dark
    
    ## Set data collection angles from proj.
    theta = tp.angles(proj.shape[0])

    ## Flat-field correction of raw data.
    proj = tp.normalize(proj, flat = flat, dark = dark)
    
    ## Additional flat-field correction of raw data to negate need to mask.
    proj = tp.normalize_bg(proj, air = 10)

    ## Set rotation center.
    rot_center = tp.find_center_vo(proj)
    print('Center of rotation: ', rot_center)
    
    tp.minus_log(proj, out = data)
    
    # Reconstruct object using Gridrec algorith.
    rec = tp.recon(proj, theta, center = rot_center, sinogram_order = False, algorithm = 'gridrec', filter_name = 'hann')
    rec = tp.remove_nan(rec)
         
    ## Writing data in netCDF3 .volume.
    ncfile = Dataset('filename.volume', 'w', format = 'NETCDF3_64BIT', clobber = True)
    NX = ncfile.createDimension('NX', rec.shape[2])
    NY = ncfile.createDimension('NY', rec.shape[1])
    NZ = ncfile.createDimension('NZ', rec.shape[0])
    volume = ncfile.createVariable('VOLUME', 'i2', ('NZ','NY','NX'))
    volume[:] = rec
    ncfile.close()


