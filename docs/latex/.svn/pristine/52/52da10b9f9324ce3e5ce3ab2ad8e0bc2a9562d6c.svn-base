#=======================================================================
# Sample Python code to write Data Exchange Format
#
# Date: 2013-04-21
# 
#=======================================================================

import h5py
import numpy as np

def write_example(filename):

    # --- prepare data ---

    # Generate fake raw data
    rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
     
    # x, y and z ranges
    x = np.arange(128)
    y = np.arange(128)
    z = np.arange(180);
   
    # --- create file ---

    # Open HDF5 file
    f = h5py.File(filename, 'w')
        
    # Create basic definitions in root
    ds = f.create_dataset('implements', data = "measurement:exchange")
      
    # --- exchange definition --- 
    
    # Exchange HDF5 group
    # /exchange
    exchangeGrp = f.create_group("exchange")
    
    # Create core HDF5 dataset in exchange group for 180 deep stack of x,y
    # images /exchange/data
    ds = exchangeGrp.create_dataset('data', data = rawdata, \
                                    compression='gzip', compression_opts=4)
 
    ds.attrs['description'] = "Projection data"
    ds.attrs['units'] = "counts"
    
    # Create HDF5 group measurement
    # /measurement
    measurementGrp = f.create_group("measurement")

    # Create HDF5 subgroup 
    # /measurement/sample
    sampleGrp = measurementGrp.create_group("sample")
    sads1 = sampleGrp.create_dataset('name', data = "Minivirus")
    sads8 = sampleGrp.create_dataset('temperature', data = 200.0, dtype='d')
    sads8.attrs['units'] = "celsius"

    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('/tmp/python/DataExchange-example3.h5')
#=======================================================================
#
#=======================================================================
