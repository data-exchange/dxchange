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

    # Open HDF5 file
    f = DataExchangeFile(filename, mode='w') 
    
    # Create core HDF5 dataset in exchange group for 180 deep stack of x,y
    # images /exchange/data
    f.add_entry( DataExchangeEntry.data(data={'value': rawdata, 'units':'counts', 'description': 'Projection Data',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )

    # Create HDF5 subgroup 
    # /measurement/sample
    f.add_entry( DataExchangeEntry.sample(name={'value': 'Minivirus'}, temperature={'value': 200.0, 'units':'celsius',
                                'dataset_opts': {'dtype': 'd'}})
    )

    # Create HDF5 subgroup 
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'APS 2-BM'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/monochromator
    f.add_entry( DataExchangeEntry.monochromator(name={'value': 'DMM'}, 
                                                energy={'value': 10.00, 'units':'keV', 'dataset_opts': {'dtype':'d'}}))

    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('./examples/DataExchange-example4.h5')
#=======================================================================
#
#=======================================================================
