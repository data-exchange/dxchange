# -*- coding: utf-8 -*-

import tomopy
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex


projections_start = 1
projections_end = 181

# read a series of tiff
file_name = '/local/dataraid/databank/CHESS/Dummy001_.tif'
mydata = dx.Import()
# Read series of images
data, white, dark, theta = mydata.series_of_images(file_name,
                                                   projections_start = projections_start,
                                                   projections_end = projections_end,
                                                   projections_digits = 4,
                                                   projections_zeros = True,
                                                   log='INFO'
                                                )

# or convert the series of tiff in data exchange
##hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/CHESS_01.h5'
##sample_name = 'Dummy'
##mydata = ex.Export()
### Create minimal data exchange hdf5 file
##mydata.xtomo_exchange(data = data,
##                      data_white = white,
##                      data_dark = dark,
##                      theta = theta,
##                      hdf5_file_name = hdf5_file_name,
##                      data_exchange_type = 'tomography_raw_projections'
##                      )

# and/or read as data exchange
# Read HDF5 file.
##data, white, dark, theta = tomopy.xtomo_reader('/local/dataraid/databank/dataExchange/microCT/CHESS_01.h5',
##                                               slices_start=100,
##                                               slices_end=101)

# Xtomo object creation and pipeline of methods.  
d = tomopy.xtomo_dataset(log='debug')
d.dataset(data, white, dark, theta)
d.normalize()
d.correct_drift()
d.optimize_center()
#d.phase_retrieval()
#d.correct_drift()
d.center=99.5
d.gridrec()


# Write to stack of TIFFs.
tomopy.xtomo_writer(d.data_recon, 'tmp/CHESS_Integrated_100_', axis=0)

