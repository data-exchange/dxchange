#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 13-BM tomography
data as original netcdf files. To use, change fname to just
the file name (e.g. 'sample[2].nc' would be 'sample'.
Reconstructed dataset will be saved as float32 netcdf3.
"""
import glob
import numpy as np
import tomopy as tp
import dxchange as dx

from netCDF4 import Dataset

if __name__ == '__main__':
    ## Set path (without file suffix) to the micro-CT data to reconstruct.
    fname = 'data_dir/sample'

    ## Import Data.
    proj, flat, dark, theta = dx.exchange.read_aps_13bm(fname, format = 'netcdf4')
     
    ## Flat-field correction of raw data.
    proj = tp.normalize(proj, flat = flat, dark = dark)

    ## Additional flat-field correction of raw data to negate need to mask.
    proj = tp.normalize_bg(proj, air = 10)

    ## Set rotation center.
    rot_center = tp.find_center_vo(proj)
    print('Center of rotation: ', rot_center)

    tp.minus_log(proj, out = proj)

    # Reconstruct object using Gridrec algorith.
    rec = tp.recon(proj, theta, center = rot_center, sinogram_order = False, algorithm = 'gridrec', filter_name = 'hann')
    rec = tp.remove_nan(rec)

    ## Writing data in netCDF3 .volume.
    ncfile = Dataset('filename.volume', 'w', format = 'NETCDF3_64BIT', clobber = True)
    NX = ncfile.createDimension('NX', rec.shape[2])
    NY = ncfile.createDimension('NY', rec.shape[1])
    NZ = ncfile.createDimension('NZ', rec.shape[0])
    volume = ncfile.createVariable('VOLUME', 'f4', ('NZ','NY','NX'))
    volume[:] = rec
    ncfile.close()
