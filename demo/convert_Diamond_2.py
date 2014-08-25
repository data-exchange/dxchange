# -*- coding: utf-8 -*-
"""
.. module:: convert_Diamond_2.py
   :platform: Unix
   :synopsis: Convert Diamond NeXuS files in data exchange.

Example on how to use the `series_of_images`_ module to read Diamond NeXuS raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

.. _series_of_images: dataexchange.xtomo.xtomo_importer.html
"""

import h5py
import numpy as np

def main():


    # Generate fake raw data
    nexus_data = np.ones(200 * 256 * 256, np.uint16).reshape(200, 256, 256)

    # Read data from file.
    file_name = '/local/data/databank/Diamond/projections_test.hdf'
    f = h5py.File(file_name, 'w')

    # Create basic definitions in root
    ds = f.create_dataset('implements', data = "exchange")
      
    # --- exchange definition --- 
    
    # Nexus entry HDF5 group
    # /entry/instrument/detector
    exchangeGrp = f.create_group("entry/instrument/detector")
    
    # Create  HDF5 dataset in entry/instrument/detector group for 200 deep stack
    # of x,y images within this stack the first 10 images are dark fields, the
    # next 10 are white fields and the rest 180 are projections
    
    ds = exchangeGrp.create_dataset('data', data = nexus_data, \
                                    compression='gzip', compression_opts=4)
 
    ds.attrs['description'] = "transmission"
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta:y:x"

    # set the reference to the 3 regions
    ref_data = ds.regionref[20:200]
    ref_data_dark = ds.regionref[0:9]
    ref_data_white = ds.regionref[10:19]

    print ref_data
    
    subset_data = ds[ref_data]
    subset_data_dark = ds[ref_data_dark]
    subset_data_white = ds[ref_data_white]
    
    subset_data = ds[ref_data]
    subset_data_dark = ds[ref_data_dark]
    subset_data_white = ds[ref_data_white]

    print subset_data.shape
    print subset_data_dark.shape
    print subset_data_white.shape


    ref_dtype = h5py.special_dtype(ref=h5py.Reference)
    ref_dataset = f.create_dataset("exchange/data", (1,), dtype=ref_dtype)
    ref_dataset_dark = f.create_dataset("exchange/data_dark", (1,), dtype=ref_dtype)
    ref_dataset_white = f.create_dataset("exchange/data_white", (1,), dtype=ref_dtype)

    # set the reference to the object
    ref_dataset[...] = ref_data
    ref_dataset_dark[...] = ref_data_dark
    ref_dataset_white[...] = ref_data_white

##    f["exchange"] = h5py.SoftLink('/entry/instrument/detector')


    print ref_data
    print ref_dataset[0]
    print ref_data_dark
    print ref_dataset_dark[0]
    print ref_data_white
    print ref_dataset_white[0]
    
    # --- All done ---
    f.close()

if __name__ == "__main__":
    main()
