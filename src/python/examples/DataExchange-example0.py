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
  
    # x, y and z ranges
    x = np.arange(256)
    y = np.arange(256)
    z = np.arange(180);
       
    # --- create file ---

    # Open DataExchange file
    f = DataExchangeFile(filename, mode='w')
        
    # Create a DataExchangeEntry and dd the entry to the data exchange file.
    f.add_entry(DataExchangeEntry.data(data={'value':rawdata, 'units':'counts'}))
                  
    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('./examples/DataExchange-example0.h5')

