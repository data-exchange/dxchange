#=======================================================================
# Sample Python code to write Data Exchange Format
#
# Date: 2013-11-05
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
      
    # --- create file ---

    # Open DataExchangeFile file
    f = DataExchangeFile(filename, mode='w')
    
    # Create core HDF5 dataset in exchange group for 180 deep stack
    # of x,y images /exchange/data
    f.add_entry([
            DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}),
            DataExchangeEntry.data(data_dark={'value':rawdata_dark, 'units':'counts'}),
            DataExchangeEntry.data(data_white={'value':rawdata_white, 'units':'counts'})
            ]
        )
                      
    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('./examples/DataExchange-example1.h5')
#=======================================================================
#
#=======================================================================
