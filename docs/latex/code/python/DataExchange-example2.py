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

    # Generate fake data
    rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
    rawdata_white = np.ones(2 * 256 * 256, np.uint16).reshape(2, 256, 256)
    rawdata_dark = np.zeros(10 * 256 * 256, np.uint16).reshape(10, 256, 256)
  
    # x, y and z ranges
    x = np.arange(256)
    y = np.arange(256)
    z = np.arange(180);
    
    # Fabricated theta values
    theta = (z / float(180)) * 180.0
    theta_white = (0.0, 180.0)
    theta_dark = (0.0, 0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0, 180.0, 180.0)
    
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
    ds.attrs['axes'] = "theta:y:x"
    
    # Create HDF5 dataset in exchange group for dark data
    # /exchange/data_dark
    ds = exchangeGrp.create_dataset('data_dark', data = rawdata_dark)
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta_dark:y:x"

    # Create HDF5 dataset in exchange group for white data
    # /exchange/data_white
    ds = exchangeGrp.create_dataset('data_white', data = rawdata_white)
    ds.attrs['units'] = "counts"
    ds.attrs['axes'] = "theta_white:y:x"
    
    # Create HDF5 dataset in exchange group for theta
    # /exchange/theta
    ds = exchangeGrp.create_dataset('theta', data = theta)
    ds.attrs['units'] = "degrees"

    # Create HDF5 dataset in exchange group for theta_dark
    # /exchange/theta_dark
    ds = exchangeGrp.create_dataset('theta_dark', data = theta_dark)
    ds.attrs['units'] = "degrees"

    # Create HDF5 dataset in exchange group for theta_white
    # /exchange/theta_white
    ds = exchangeGrp.create_dataset('theta_white', data = theta_white)
    ds.attrs['units'] = "degrees"
                  
    # --- All done ---
    f.close()

if __name__ == '__main__':
    write_example('/tmp/python/DataExchange-example2.h5')
#=======================================================================
#
#=======================================================================
