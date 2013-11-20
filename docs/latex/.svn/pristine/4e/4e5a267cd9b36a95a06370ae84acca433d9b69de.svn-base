#=======================================================================
# Sample Python code to write Data Exchange Format
#
# Date: 2011-09-01
# Updated: 2013-04-21
#=======================================================================

import h5py
import numpy as np

def write_example(filename):

    # --- prepare data ---

    # Generate fake data
    rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
  
    # x, y and z ranges
    x = np.arange(256)
    y = np.arange(256)
    z = np.arange(180);
       
    # --- create file ---

    # Open HDF5 file
    f = h5py.File(filename, 'w')
        
    # Create basic definitions in root
    ds = f.create_dataset('implements', data = "exchange")
    
    # --- exchange definition --- 
    
    # Exchange HDF5 group
    # /exchange
    exchangeGrp = f.create_group("exchange")
    
    # Create core HDF5 dataset in exchange group for 180 deep stack
    # of x,y images /exchange/data
    ds = exchangeGrp.create_dataset('data', data = rawdata)
    ds.attrs['units'] = "counts"
                  
    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('/tmp/python/DataExchange-example0.h5')
#=======================================================================
#
#=======================================================================
