# -*- coding: utf-8 -*-

import tomopy
import dataexchange.xtomo.xtomo_importer as dx
import dataexchange.xtomo.xtomo_exporter as ex

def main():

    file_name = '/local/dataraid/databank/CHESS/scan1/scan1_.tiff'
    dark_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_dark_.tiff'
    white_file_name = '/local/dataraid/databank/CHESS/scan1/scan1_white_.tiff'

    hdf5_file_name = '/local/dataraid/databank/dataExchange/microCT/CHESS_02.h5'
    sample_name = 'Dummy'

    projections_start = 1
    projections_end = 361
    white_start = 0
    white_end = 1
    white_step = 1
    dark_start = 0
    dark_end = 1
    dark_step = 1


    # set to convert slices between slices_start and slices_end
    # if omitted all data set will be converted   
    slices_start = 400    
    slices_end = 405    

    mydata = dx.Import()
    # Read series of images
    data, white, dark, theta = mydata.series_of_images(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       slices_start = slices_start,
                                                       slices_end = slices_end,
                                                       sample_name = sample_name,
                                                       projections_digits = 3,
                                                       projections_zeros = True,
                                                       log='INFO'
                                                    )    
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
    #d.center=99.5
    d.gridrec()


    # Write to stack of TIFFs.
    tomopy.xtomo_writer(d.data_recon, 'tmp/CHESS_scan1_', axis=0)

if __name__ == "__main__":
    main()

