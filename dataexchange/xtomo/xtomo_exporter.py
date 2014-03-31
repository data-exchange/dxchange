# -*- coding: utf-8 -*-
import numpy as np
import os
import h5py
import logging

from formats.data_exchange.data_exchange import DataExchangeFile, DataExchangeEntry

class Export():
    def __init__(xtomo, data=None, data_white=None, 
                 data_dark=None, theta=None,
                 hdf5_file_name=None, data_exchange_type=None,
                 sample_name=None, logger=None, log='INFO'):

        xtomo.data = data
        xtomo.data_white = data_white
        xtomo.data_dark = data_dark
        xtomo.theta = theta

    def xtomo_writer(data, output_file=None, x_start=0,
                     digits=5, axis=0, overwrite=False, 
                     precision=True):
        """ 
        Write 3-D data to a stack of tif files.

        Parameters
        -----------
        output_file : str, optional
            Name of the output file.

        x_start : scalar, optional
            First index of the data on first dimension
            of the array.

        digits : scalar, optional
            Number of digits used for file indexing.
            For example if 4: test_XXXX.tiff
            
        axis : scalar, optional
            Imaages is read along that axis.
            
        overwrite: bool, optional
            if overwrite=True the existing data in the
            reconstruction folder will be overwritten
            
        precision : bool, optional
            Export data type precision. if True it 
            saves 32-bit precision. Otherwise it
            uses 8-bit precision.
        
        Notes
        -----
        If file exists, saves it with a modified name.
        
        If output location is not specified, the data is
        saved inside ``recon`` folder where the input data
        resides. The name of the reconstructed files will
        be initialized with ``recon``
        
        Examples
        --------
        - Save sinogram data:
            
            >>> import tomopy
            >>> 
            >>> # Load data
            >>> myfile = 'demo/data.h5'
            >>> data, white, dark, theta = tomopy.xtomo_reader(myfile)
            >>> 
            >>> # Save data
            >>> output_file='tmp/slice_'
            >>> tomopy.xtomo_writer(data, output_file, axis=1)
            >>> print "Images are succesfully saved at " + output_file + '...'
            
        - Save first 16 projections:
            
            >>> import tomopy
            >>> 
            >>> # Load data
            >>> myfile = 'demo/data.h5'
            >>> data, white, dark, theta = tomopy.xtomo_reader(myfile, projections_start=0, projections_end=16)
            >>> 
            >>> # Save data
            >>> output_file='tmp/projection_'
            >>> tomopy.xtomo_writer(data, output_file, axis=0)
            >>> print "Images are succesfully saved at " + output_file + '...'
            
        - Save reconstructed slices:
            
            >>> import tomopy
            >>> 
            >>> # Load data
            >>> myfile = 'demo/data.h5'
            >>> data, white, dark, theta = tomopy.xtomo_reader(myfile)
            >>> 
            >>> # Perform reconstruction
            >>> d = tomopy.xtomo_dataset(log='error')
            >>> d.dataset(data, white, dark, theta)
            >>> d.center = 661.5
            >>> d.gridrec()
            >>> 
            >>> # Save data
            >>> output_file='tmp/reconstruction_'
            >>> tomopy.xtomo_writer(d.data_recon, output_file, axis=0)
            >>> print "Images are succesfully saved at " + output_file + '...'
        """
        if output_file == None:
            output_file = "tmp/img_" 
        output_file =  os.path.abspath(output_file)
        dir_path = os.path.dirname(output_file)
        
        # Remove TIFF extension if there is.
        if (output_file.endswith('tif') or
            output_file.endswith('tiff')) :
                output_file = output_file.split(".")[-2]
      
        if overwrite:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                
        # Create new folders.
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Select desired x from whole data.
        num_x, num_y, num_z = data.shape
        if axis == 0:
            x_end = x_start+num_x
        elif axis == 1:
            x_end = x_start+num_y
        elif axis == 2:
            x_end = x_start+num_z

        # Write data.
        file_index = ["" for x in range(digits)]
        for m in range(digits):
            file_index[m] = '0' * (digits - m - 1)
        ind = range(x_start, x_end)
        for m in range(len(ind)):
            for n in range(digits):
                if ind[m] < np.power(10, n + 1):
                    file_body = output_file + file_index[n] + str(ind[m])
                    file_name = file_body + '.tif'
                    break
            if precision:
                if axis == 0:
                    img = misc.toimage(data[m, :, :], mode='F')
                elif axis == 1:
                    img = misc.toimage(data[:, m, :], mode='F')
                elif axis == 2:
                    img = misc.toimage(data[:, :, m], mode='F')
            else:
                if axis == 0:
                    img = misc.toimage(data[m, :, :])
                elif axis == 1:
                    img = misc.toimage(data[:, m, :])
                elif axis == 2:
                    img = misc.toimage(data[:, :, m])

            # check if file exists.
            if os.path.isfile(file_name):
                # genarate new file name.
                indq = 1
                FLAG_SAVE = False
                while not FLAG_SAVE:
                    new_file_body = file_body + '-' + str(indq)
                    new_file_name = new_file_body + '.tif'
                    if not os.path.isfile(new_file_name):
                        img.save(new_file_name)
                        FLAG_SAVE = True
                        file_name = new_file_name
                    else:
                        indq += 1
            else:
                img.save(file_name)        

    def data_exchange(xtomo,
                      sample_name=None,
                      data_exchange_type=None,
                      hdf5_file_name=None):
        """
        Save Data Exchange HDF5 file.
        
        Parameters
        ----------
        xtomo : tomopy data object
            This is the core X-ray absorption tomography
            data object that all low-level
            attributes and methods are bound to.
            
        data : ndarray
            3-D X-ray absorption tomography raw data.
            Size of the dimensions should be:
            [projections, slices, pixels].
            
        data_white, data_dark : ndarray, optional
            3-D white-field/dark_field data. Multiple
            projections are stacked together to obtain
            a 3-D matrix. 2nd and 3rd dimensions should
            be the same as data: [shots, slices, pixels].
            
        theta : ndarray, optional
            Data acquisition angles corresponding
            to each projection.
        data_excahnge_type : str
            label defyining the type of data contained in data exchange file
            for raw data tomography data use 'tomography_raw_projections'

        hd5_file_name : str
            Output file.
        """

        xtomo.logger.info("Creating Data Exchange File [%s]", hdf5_file_name)

        
##        if (hdf5_file_name != None):
##            if os.path.isfile(hdf5_file_name):
##                xtomo.logger.info("Data Exchange file already exists: [%s]. Next time use the Data Exchange reader instead", hdf5_file_name)
##            else:
##                # Create new folder.
##                dirPath = os.path.dirname(hdf5_file_name)
##                if not os.path.exists(dirPath):
##                    os.makedirs(dirPath)
##
##                # Get the file_name in lower case.
##                lFn = hdf5_file_name.lower()
##
##                # Split the string with the delimeter '.'
##                end = lFn.split('.')
##
##                # Write the Data Exchange HDF5 file.
##                # Open DataExchange file
##                f = DataExchangeFile(hdf5_file_name, mode='w') 
##
##                xtomo.logger.info("Creating Data Exchange File [%s]", hdf5_file_name)
##
##                # Create core HDF5 dataset in exchange group for projections_theta_range
##                # deep stack of x,y images /exchange/data
##                xtomo.logger.info("Adding projections to Data Exchange File [%s]", hdf5_file_name)
##                f.add_entry( DataExchangeEntry.data(data={'value': data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
##                if (xtomo.theta != None):
##                    f.add_entry( DataExchangeEntry.data(theta={'value': xtomo.theta, 'units':'degrees'}))
##                    xtomo.logger.info("Adding theta to Data Exchange File [%s]", hdf5_file_name)
##                if (xtomo.data_dark != None):
##                    xtomo.logger.info("Adding dark fields to  Data Exchange File [%s]", hdf5_file_name)
##                    f.add_entry( DataExchangeEntry.data(data_dark={'value': xtomo.data_dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
##                if (xtomo.data_white != None):
##                    xtomo.logger.info("Adding white fields to  Data Exchange File [%s]", hdf5_file_name)
##                    f.add_entry( DataExchangeEntry.data(data_white={'value': xtomo.data_white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
##                if (data_exchange_type != None):
##                    xtomo.logger.info("Adding data type to  Data Exchange File [%s]", hdf5_file_name)
##                    f.add_entry( DataExchangeEntry.data(title={'value': data_exchange_type}))
##                if (sample_name == None):
##                    sample_name = end[0]
##                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 file name'}))
##                else:
##                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
##                f.close()
##                xtomo.logger.info("DONE!!!!. Created Data Exchange File [%s]", hdf5_file_name)                
