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

    # Generate fake raw data
    rawdata = np.ones(180 * 256 * 256, np.uint16).reshape(180, 256, 256)
     
    # x, y and z ranges
    x = np.arange(128)
    y = np.arange(128)
    z = np.arange(180);
   
    # --- create file ---

    # Open DataExchange file
    f = DataExchangeFile(filename, mode='w')
    
    # Create core HDF5 dataset in exchange group for 180 deep stack of x,y
    # images /exchange/data
    data_en = DataExchangeEntry.data(data={'value': rawdata, 'units':'counts', 'description': 'Projection Data',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    f.add_entry(data_en)

    # The default location for sample in DataExchangeEntry is /measurement/sample
    # To override the default set e.g 'root'='/measurement_4/sample'
    sample_en = DataExchangeEntry.sample(name={'value': 'Minivirus'}, temperature={'value': 200.0, 'units':'celsius',
                                'dataset_opts': {'dtype': 'd'}})
    f.add_entry(sample_en)

    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('./examples/DataExchange-example3.h5')
#=======================================================================
#
#=======================================================================
