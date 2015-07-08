#=======================================================================
# Sample Python code to write Data Exchange Format
#
# Date: 2013-04-21
# 
#=======================================================================

from data_exchange import DataExchangeFile, DataExchangeEntry
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
    f = DataExchangeFile(filename, mode='w')

    #Create HDF5 dataset in exchange group for data, data_dark & data_white, theta, theta_dark, theta_white under /exchange
    f.add_entry([
            DataExchangeEntry.data(data={'value':rawdata, 'units':'counts', 'axes': 'theta:y:x'}),
            DataExchangeEntry.data(data_dark={'value':rawdata_dark, 'units':'counts', 'axes': 'theta:y:x'}),
            DataExchangeEntry.data(data_white={'value':rawdata_white, 'units':'counts', 'axes': 'theta:y:x'}),
            DataExchangeEntry.data(theta={'value':theta, 'units':'degrees'}),
            DataExchangeEntry.data(theta_dark={'value':theta_dark, 'units':'degrees'}),
            DataExchangeEntry.data(theta_white={'value':theta_white, 'units':'degrees'})
        ])
                  
    # --- All done ---
    f.close()

if __name__ == '__main__':
    write_example('./examples/DataExchange-example2.h5')
#=======================================================================
#
#=======================================================================
