#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 5-BM data as original xmt.
xmt are 16 bit unsigned integer tiff file that requires a byte swap before
being processed.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    fname = 'data_dir/'

    # Select the sinogram range to reconstruct.
    start = 290
    end = 294

    # Read the APS 5-BM raw data
    proj, flat, dark = dxchange.read_aps_5bm(fname, sino=(start, end))

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    # remove stripes
    proj = tomopy.remove_stripe_fw(proj,level=7,wname='sym16',sigma=1,pad=True)

    # Set rotation center.
    rot_center = proj.shape[2] / 2.0
    print("Center of rotation: ", rot_center)

    proj = tomopy.minus_log(proj)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/recon')
