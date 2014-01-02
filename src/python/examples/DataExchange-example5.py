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
    rawdata_white = np.ones(2 * 256 * 256, np.uint16).reshape(2, 256, 256)
    rawdata_dark = np.zeros(10 * 256 * 256, np.uint16).reshape(10, 256, 256)

    # Generate fake normalized data
    normalizeddata = np.ones(180 * 256 * 256, \
                             np.float64).reshape(180, 256, 256)

    # Generate fake reconstructed data
    reconstructeddata = np.ones(256 * 256 * 256, \
                                np.float64).reshape(256, 256, 256)
     
    # x, y and z ranges
    x = np.arange(128)
    y = np.arange(128)
    z = np.arange(180);
    
    # Fabricated theta values
    theta = (z / float(180)) * 180.0
    theta_white = (0.0, 180.0)
    theta_dark = (0.0, 0.0, 0.0, 0.0, 0.0, 180.0, 180.0, 180.0, 180.0, 180.0)

    # Fabricated data_shift_x and data_shift_y value
    data_shift_x = np.random.randint(-100, 100, size=180) 
    data_shift_y = np.random.randint(-100, 100, size=180) 

    # --- create file ---

    print filename
    
    # Open DataExchange file
    f = DataExchangeFile(filename, mode='w') 
        
    
    # Create core HDF5 dataset in exchange group for 180 deep stack
    # of x,y images /exchange/data
    f.add_entry( DataExchangeEntry.data(data={'value': rawdata, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )
    f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
    f.add_entry( DataExchangeEntry.data(data_dark={'value':rawdata_dark, 'units':'counts', 'axes':'theta_dark:y:x',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )
    f.add_entry( DataExchangeEntry.data(data_white={'value': rawdata_white, 'units':'counts', 'axes':'theta_white:y:x',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )
    f.add_entry( DataExchangeEntry.data(theta={'value': theta, 'units':'degrees'}))
    f.add_entry( DataExchangeEntry.data(theta_dark={'value': theta_dark, 'units':'degrees'}))
    f.add_entry( DataExchangeEntry.data(theta_white={'value': theta_white, 'units':'degrees'}))
    f.add_entry( DataExchangeEntry.data(data_shift_x={'value': data_shift_x}))
    f.add_entry( DataExchangeEntry.data(data_shift_y={'value': data_shift_y}))
                  
    # Exchange HDF5 group
    # /exchange_2
    # this will be the out_put of the normalization process
    f.add_entry( DataExchangeEntry.data(root='exchange_2', title={'value': 'tomography normalized projections'}) )
    f.add_entry( DataExchangeEntry.data(root='exchange_2', data={'value': normalizeddata, 'units':'counts', 'axes':'theta:y:x',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )
    f.add_entry( DataExchangeEntry.data(root='exchange_2', theta={'value': theta, 'units':'degrees'}))

    # Exchange HDF5 group
    # /exchange_3
    # this will be the out_put of the reconstruction process
    f.add_entry( DataExchangeEntry.data(root='exchange_3', title={'value': 'tomography reconstructions'}) )
    f.add_entry( DataExchangeEntry.data(root='exchange_3', data={'value': reconstructeddata, 'units':'density', 'axes':'z:y:x',
                                            'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} })
    )

    # Create HDF5 group measurement
    # /measuremen
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'APS 2-BM'}) )

    # Create HDF5 subgroup
    # /measurement/instrument/source
    f.add_entry( DataExchangeEntry.source(name={'value': 'APS'}, 
                                        date_time={'value': "2012-07-31T21:15:23+0600"},
                                        beamline={'value': "2-BM"}, 
                                        current={'value': 101.199, 'units': 'mA', 'dataset_opts':  {'dtype': 'd'}},
                                        energy={'value': 7.0, 'units':'GeV', 'dataset_opts':  {'dtype': 'd'}},
                                        mode={'value':'TOPUP'}
                                        )
    )
    # Create HDF5 subgroup
    # /measurement/instrument/attenuator           
    f.add_entry( DataExchangeEntry.attenuator(thickness={'value': 1e-3, 'units': 'm', 'dataset_opts':  {'dtype': 'd'}},
                                            type={'value': 'Al'}
                                            )
        )

    # Create HDF5 subgroup
    # /measurement/instrument/monochromator
    f.add_entry( DataExchangeEntry.monochromator(type={'value': 'Multilayer'},
                                                energy={'value': 19.26, 'units': 'keV', 'dataset_opts':  {'dtype': 'd'}},
                                                energy_error={'value': 1e-3, 'units': 'keV', 'dataset_opts':  {'dtype': 'd'}},
                                                mono_stripe={'value': 'Ru/C'},
                                                )
        )                                                                                                                                                                                                                                                                                                                                                                                                         

    # Create HDF5 subgroup
    # /measurement/instrument/detector
    f.add_entry( DataExchangeEntry.detector(manufacturer={'value':'CooKe Corporation'},
                                            model={'value': 'pco dimax'},
                                            serial_number={'value': '1234XW2'},
                                            bit_depth={'value': 12, 'dataset_opts':  {'dtype': 'd'}},
                                            x_pixel_size={'value': 6.7e-6, 'dataset_opts':  {'dtype': 'f'}},
                                            y_pixel_size={'value': 6.7e-6, 'dataset_opts':  {'dtype': 'f'}},
                                            x_dimensions={'value': 2048, 'dataset_opts':  {'dtype': 'i'}},
                                            y_dimensions={'value': 2048, 'dataset_opts':  {'dtype': 'i'}},
                                            x_binning={'value': 1, 'dataset_opts':  {'dtype': 'i'}},
                                            y_binning={'value': 1, 'dataset_opts':  {'dtype': 'i'}},
                                            operating_temperature={'value': 270, 'units':'K', 'dataset_opts':  {'dtype': 'f'}},
                                            exposure_time={'value': 170, 'units':'ms', 'dataset_opts':  {'dtype': 'd'}},
                                            frame_rate={'value': 3, 'dataset_opts':  {'dtype': 'i'}},
                                            output_data={'value':'/exchange'}
                                            )
        )

    f.add_entry( DataExchangeEntry.roi(name={'value':'Center Third'},
                                        x1={'value':256, 'dataset_opts':  {'dtype': 'i'}},
                                        x2={'value':1792, 'dataset_opts':  {'dtype': 'i'}},
                                        y1={'value':256, 'dataset_opts':  {'dtype': 'i'}},
                                        y2={'value':1792, 'dataset_opts':  {'dtype': 'i'}},
                                        )
        )

    f.add_entry(DataExchangeEntry.objective(manufacturer={'value':'Zeiss'},
                                            model={'value':'Plan-NEOFLUAR 1004-072'},
                                            magnification={'value':20, 'dataset_opts':  {'dtype': 'd'}},
                                            numerical_aperture={'value':0.5, 'dataset_opts':  {'dtype': 'd'}},
                                        )
        )

    f.add_entry(DataExchangeEntry.scintillator(manufacturer={'value':'Crytur'},
                                                serial_number={'value':'12'},
                                                name={'value':'YAG polished'},
                                                type={'value':'YAG on YAG'},
                                                scintillating_thickness={'value':5e-6, 'dataset_opts':  {'dtype': 'd'}},
                                                substrate_thickness={'value':1e-4, 'dataset_opts':  {'dtype': 'd'}},
            )
        )


    # Create HDF5 subgroup 
    # /measurement/sample
    f.add_entry( DataExchangeEntry.sample( name={'value':'Hornby_b'},
                                            description={'value':'test sample'},
                                            preparation_date={'value':'2011-07-31T21:15:23+0600'},
                                            chemical_formula={'value':'unknown'},
                                            mass={'value':0.25, 'units':'g', 'dataset_opts':  {'dtype': 'd'}},
                                            enviroment={'value':'air'},
                                            temperature={'value':120.0, 'units':'Celsius', 'dataset_opts':  {'dtype': 'd'}},
                                            temperature_set={'value':130.0, 'units':'Celsius', 'dataset_opts':  {'dtype': 'd'}},
            )
        )

    # Create HDF5 subgroup 
    # /measurement/sample/geometry/translation
    f.add_entry( DataExchangeEntry.translation(root='/measurement/sample/geometry',
                    distances={'value':[0,0,0],'axes':'z:y:x', 'units':'m', 'dataset_opts':  {'dtype': 'd'}}
                    )
        )
    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"John Doe"},
                                                role={'value':"Project PI"},
                                                affiliation={'value':"University of California, Berkeley"},
                                                address={'value':"EPS UC Berkeley CA 94720 4767 USA"},
                                                phone={'value':"+1 123 456 0000"},
                                                email={'value':"johndoe@berkeley.edu"},
                                                facility_user_id={'value':"a123456"},

                    )
        )
    

    # Create HDF5 subgroup
    # /measurement/experiment
    f.add_entry( DataExchangeEntry.experiment(  proposal={'value':"1234"},
                                                activity={'value':"e11218"},
                                                safety={'value':"9876"},
                )
        )

    # --- All done ---
    f.close()

if __name__ == '__main__':
    
    write_example('DataExchange-example5.h5')
#    write_example('./examples/DataExchange-example5.h5')
#=======================================================================
#
#=======================================================================
