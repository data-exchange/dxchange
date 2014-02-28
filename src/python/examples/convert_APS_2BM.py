# -*- coding: utf-8 -*-
"""
.. module:: main_convert_APS_2BM.py
   :platform: Unix
   :synopsis: Convert APS 2-BM HDF4 files in data exchange.

.. moduleauthor:: Francesco De Carlo <decarlof@gmail.com>


""" 
from data_exchange import DataExchangeFile, DataExchangeEntry
from data_exchange.data_convert import Convert

import re

import logging
logging.basicConfig(filename='convert_APS_2BM.log',level=logging.DEBUG)

def main():

    file_name = '/local/data/Hornby_APS/Hornby_19keV_10x_.hdf'
    hdf5_file_name = '/local/data/Hornby_APS/Hornby_19keV_10x_APS_2011.h5'

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = 1503
    dark_start = 1504
    dark_end = 1505

    mydata = Convert()
    # Create minimal hdf5 file
    mydata.series_of_images(file_name,
                     hdf5_file_name,
                     projections_start,
                     projections_end,
                     white_start = white_start,
                     white_end = white_end,
                     dark_start = dark_start,
                     dark_end = dark_end,
                     projections_digits = 5,
                     data_type = 'hdf4',
                 )

     
    # Add extra metadata if available / desired

    # Open DataExchange file
    f = DataExchangeFile(hdf5_file_name, mode='a') 

    # Create HDF5 subgroup
    # /measurement/instrument
    f.add_entry( DataExchangeEntry.instrument(name={'value': 'APS 2-BM'}) )

    f.add_entry( DataExchangeEntry.source(name={'value': 'Advanced Photon Source'},
                                        date_time={'value': "2012-07-31T21:15:23+0600"},
                                        beamline={'value': "2-BM"},
                                        current={'value': 101.199, 'units': 'mA', 'dataset_opts': {'dtype': 'd'}},
                                        energy={'value': 7.0, 'units':'GeV', 'dataset_opts': {'dtype': 'd'}},
                                        mode={'value':'TOPUP'}
                                        )
    )
    # Create HDF5 subgroup
    # /measurement/instrument/attenuator
    f.add_entry( DataExchangeEntry.attenuator(thickness={'value': 1e-3, 'units': 'm', 'dataset_opts': {'dtype': 'd'}},
                                            type={'value': 'Al'}
                                            )
        )

    # Create HDF5 subgroup
    # Create HDF5 subgroup
    # /measurement/instrument/monochromator
    f.add_entry( DataExchangeEntry.monochromator(type={'value': 'Multilayer'},
                                                energy={'value': 19.26, 'units': 'keV', 'dataset_opts': {'dtype': 'd'}},
                                                energy_error={'value': 1e-3, 'units': 'keV', 'dataset_opts': {'dtype': 'd'}},
                                                mono_stripe={'value': 'Ru/C'},
                                                )
        )


    # Create HDF5 subgroup
    # /measurement/experimenter
    f.add_entry( DataExchangeEntry.experimenter(name={'value':"Jane Waruntorn"},
                                                role={'value':"Project PI"},
                                                affiliation={'value':"University of California"},
                                                facility_user_id={'value':"64924"},

                    )
        )

    f.add_entry(DataExchangeEntry.objective(manufacturer={'value':'Zeiss'},
                                            model={'value':'Plan-NEOFLUAR 1004-072'},
                                            magnification={'value':5, 'dataset_opts': {'dtype': 'd'}},
                                            numerical_aperture={'value':0.5, 'dataset_opts': {'dtype': 'd'}},
                                        )
        )

    f.add_entry(DataExchangeEntry.scintillator(manufacturer={'value':'Crytur'},
                                                serial_number={'value':'12'},
                                                name={'value':'LuAg '},
                                                type={'value':'LuAg'},
                                                scintillating_thickness={'value':50e-6, 'dataset_opts': {'dtype': 'd'}},
                                                substrate_thickness={'value':50e-6, 'dataset_opts': {'dtype': 'd'}},
            )
        )

    # Create HDF5 subgroup
    # /measurement/experiment
    f.add_entry( DataExchangeEntry.experiment( proposal={'value':"GUP-34353"},
                                                activity={'value':"32-IDBC-2013-106491"},
                                                safety={'value':"106491-49734"},
                )
        )

    f.close()
    print "Done converting ", hdf5_file_name

if __name__ == "__main__":
    main()

