#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the ALS tomography
beamline 8.3.2 data as original hdf5.
"""
from __future__ import print_function
import tomopy
import dxchange


if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    fname = 'data_dir/sample.h5'

    # Select the sinogram range to reconstruct.
    start = 0
    end = 16

    # Read the ALS raw data.
    proj, flat, dark = dxchange.read_als_832h5(fname, sino=(start, end))

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], 0, 180)

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    # Find rotation center.
    rot_center = tomopy.find_center(proj, theta, emission=False, init=1024, ind=0, tol=0.5)
    print("Center of rotation:", rot_center)

    tomopy.minus_log(proj)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/als_')
