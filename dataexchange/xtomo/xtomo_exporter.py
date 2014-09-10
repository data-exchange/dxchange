# -*- coding: utf-8 -*-
import numpy as np
import os
import h5py
import logging
import warnings
from skimage import io as skimage_io 

from data_exchange import DataExchangeFile, DataExchangeEntry

class Export():
    def __init__(self, data=None, data_white=None, 
                 data_dark=None, theta=None,
                 hdf5_file_name=None, data_exchange_type=None,
                 sample_name=None, logger=None, log='INFO'):

        # Set the log level.
        self.logger = None
        self._log_level = str(log).upper()
        self._init_logging()

    def xtomo_tiff(self, data, output_file=None, x_start=0,
                     digits=5, axis=0, overwrite=False, delete=False,
                     dtype='float32', data_min=None, data_max=None):
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
            if overwrite=True the existing files in the
            reconstruction folder will be overwritten
            with the new ones.
            
        delete: bool, optional
            if delete=True the reconstruction
            folder and its contents will be deleted.
            
        dtype : bool, optional
            Export data type precision.
            
        data_min, data_max : scalar, optional
            User defined minimum and maximum values
            in the data that will be used to scale 
            the dataset when saving.
        
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
            
            >>> import dataexchange.xtomo.xtomo_importer as dx
            >>> import dataexchange.xtomo.xtomo_exporter as ex
            >>> 
            >>> file_name = '/local/dataraid/databank/dataExchange/microCT/Elettra.h5'
            >>> file_name_out = 'tmp/sinogram_'
            >>>     
            >>> # Load data
            >>> mydata = dx.Import()
            >>> # Read series of images
            >>> data, white, dark, theta = mydata.xtomo_raw(file_name, data_type='h5', slices_start=0, slices_end=16)
            >>> 
            >>> # Save data
            >>> mydata = ex.Export()
            >>> mydata.xtomo_tiff(data = data, output_file = file_name_out, axis=1)
            >>>             
        - Save first 16 projections:
            
            >>> import dataexchange.xtomo.xtomo_importer as dx
            >>> import dataexchange.xtomo.xtomo_exporter as ex
            >>> 
            >>> file_name = '/local/dataraid/databank/dataExchange/microCT/Elettra.h5'
            >>> file_name_out = 'tmp/projection_'
            >>> 
            >>> # Load data
            >>> mydata = dx.Import()
            >>> # Read series of images
            >>> data, white, dark, theta = mydata.xtomo_raw(file_name, data_type='h5', projections_start=0, projections_end=16)

            >>> # Save data
            >>> mydata = ex.Export()
            >>> mydata.xtomo_tiff(data = data, output_file = file_name_out, axis=0)
            
        - Save reconstructed slices:
            
            >>> import tomopy 
            >>> import dataexchange.xtomo.xtomo_importer as dx
            >>> import dataexchange.xtomo.xtomo_exporter as ex

            >>> hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Elettra.h5'
            >>> mydata = dx.Import()
            >>> data, white, dark, theta = mydata.xtomo_raw(hdf5_file_name, slices_start = 150, slices_end = 154, data_type='h5', log='INFO')
            >>> d = tomopy.xtomo_dataset(log='debug')
            >>> d.dataset(data, white, dark, theta)
            >>> d.normalize()
            >>> d.correct_drift()
            >>> d.optimize_center()
            >>> d.gridrec()
            >>> 
            >>> # Save data
            >>> mydata = ex.Export()
            >>> mydata.xtomo_tiff(data = d.data_recon, output_file = 'tmp/Elettra_dataExchange_2_tomoPy_', axis=0)
        """
        output_file =  os.path.abspath(output_file)
        dir_path = os.path.dirname(output_file)
            
        # Find max min of data for scaling
        if data_max is None:
            data_max = np.max(data)
        if data_min is None:
            data_min = np.min(data)
            
        if data_max < np.max(data):
            data[data>data_max] = data_max
        if data_min > np.min(data):
            data[data<data_min] = data_min
        
        # Remove TIFF extension if there is.
        if (output_file.endswith('tif') or
            output_file.endswith('tiff')) :
                output_file = output_file.split(".")[-2]
      
        if delete:
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

            # check if file exists.
            if not overwrite:
                new_file_name = file_name
                if os.path.isfile(file_name):
                    self.logger.warning("File [%s] exists", file_name)
                    # generate new file unique name.
                    indq = 1
                    FLAG_SAVE = False
                    while not FLAG_SAVE:
                        new_file_body = file_body + '-' + str(indq)
                        new_file_name = new_file_body + '.tif'
                        if not os.path.isfile(new_file_name):
                            #self.logger.warning("File [%s] exists", new_file_name)
                            FLAG_SAVE = True
                            file_name = new_file_name
                        else:
                            self.logger.warning("File [%s] exists", new_file_name)
                            indq += 1

            if axis == 0:
                arr = data[m, :, :]
            elif axis == 1:
                arr = data[:, m, :]
            elif axis == 2:
                arr = data[:, :, m]

            if dtype is 'uint8':
                arr = ((arr*1.0 - data_min)/(data_max-data_min)*255).astype('uint8')
            elif dtype is 'uint16':
                arr = ((arr*1.0 - data_min)/(data_max-data_min)*65535).astype('uint16')
            elif dtype is 'float32':
                arr = arr.astype('float32')

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.logger.info("File saved as [%s]", new_file_name)
                skimage_io.imsave(file_name, arr, plugin='tifffile')

        self.logger.info("File conversion is complete")

    def xtomo_exchange(self, data, data_white=None, data_dark=None, theta=None, sample_name=None,
                       data_exchange_type=None,
                       hdf5_file_name=None,
                       log='INFO'
                       ):
        """ 
        Write 3-D data to a data-exchange file.

        Parameters
        ----------            
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

        Notes
        -----
        If file exists, does nothing
                
        Examples
        --------
        - Convert tomographic projection series (raw, dark, white)  of tiff in data exchange:
            
            >>> from dataexchange import xtomo_importer as dx
            >>> from dataexchange import xtomo_exporter as ex

            >>> file_name = '/local/dataraid/databank/Anka/radios/image_.tif'
            >>> dark_file_name = '/local/dataraid/databank/Anka/darks/image_.tif'
            >>> white_file_name = '/local/dataraid/databank/Anka/flats/image_.tif'

            >>> hdf5_file_name = '/local/dataraid/databank/dataExchange/tmp/Anka.h5'

            >>> projections_start = 0
            >>> projections_end = 3167
            >>> white_start = 0
            >>> white_end = 100
            >>> dark_start = 0
            >>> dark_end = 100

            >>> sample_name = 'Anka'
            >>> 
            >>> mydata = dx.Import()
            >>> # Read series of images
            >>> data, white, dark, theta = mydata.xtomo_raw(file_name,
            >>>                                                    projections_start = projections_start,
            >>>                                                    projections_end = projections_end,
            >>>                                                    white_file_name = white_file_name,
            >>>                                                    white_start = white_start,
            >>>                                                    white_end = white_end,
            >>>                                                    dark_file_name = dark_file_name,
            >>>                                                    dark_start = dark_start,
            >>>                                                    dark_end = dark_end,
            >>>                                                    projections_digits = 5,
            >>>                                                    log='INFO'
            >>>                                                    )

            >>> mydata = ex.Export()
            >>> # Create minimal data exchange hdf5 file
            >>> mydata.xtomo_exchange(data = data,
            >>>                       data_white = white,
            >>>                       data_dark = dark,
            >>>                       theta = theta,
            >>>                       hdf5_file_name = hdf5_file_name,
            >>>                       data_exchange_type = 'tomography_raw_projections',
            >>>                       sample_name = sample_name
            >>>                       )

        """
     
        if (hdf5_file_name != None):
            if os.path.isfile(hdf5_file_name):
                self.logger.error("Data Exchange file: [%s] already exists", hdf5_file_name)
            else:
                # Create new folder.
                dirPath = os.path.dirname(hdf5_file_name)
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)

                # Get the file_name in lower case.
                lFn = hdf5_file_name.lower()

                # Split the string with the delimeter '.'
                end = lFn.split('.')

                # Write the Data Exchange HDF5 file.
                # Open DataExchange file
                f = DataExchangeFile(hdf5_file_name, mode='w') 

                self.logger.info("Creating Data Exchange File [%s]", hdf5_file_name)

                # Create core HDF5 dataset in exchange group for projections_theta_range
                # deep stack of x,y images /exchange/data
                self.logger.info("Adding projections to Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data={'value': data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x' }))
#                f.add_entry( DataExchangeEntry.data(data={'value': data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                if (theta != None):
                    f.add_entry( DataExchangeEntry.data(theta={'value': theta, 'units':'degrees'}))
                    self.logger.info("Adding theta to Data Exchange File [%s]", hdf5_file_name)
                else:
                    self.logger.warning("theta is not defined")
                if (data_dark != None):
                    self.logger.info("Adding dark fields to  Data Exchange File [%s]", hdf5_file_name)
                    f.add_entry( DataExchangeEntry.data(data_dark={'value': data_dark, 'units':'counts', 'axes':'theta_dark:y:x' }))
#                    f.add_entry( DataExchangeEntry.data(data_dark={'value': data_dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                else:
                    self.logger.warning("data dark is not defined")
                if (data_white != None):
                    self.logger.info("Adding white fields to  Data Exchange File [%s]", hdf5_file_name)
                    f.add_entry( DataExchangeEntry.data(data_white={'value': data_white, 'units':'counts', 'axes':'theta_white:y:x' }))
#                    f.add_entry( DataExchangeEntry.data(data_white={'value': data_white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                else:
                    self.logger.warning("data white is not defined")
                if (data_exchange_type != None):
                    self.logger.info("Adding data type to  Data Exchange File [%s]", hdf5_file_name)
                    f.add_entry( DataExchangeEntry.data(title={'value': data_exchange_type}))
                if (sample_name == None):
                    sample_name = end[0]
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 file name'}))
                else:
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                f.close()
                self.logger.info("DONE!!!!. Created Data Exchange File [%s]", hdf5_file_name)
        else:
            self.logger.warning("Nothing to do ...")
            

    def _init_logging(self):
        """
        Setup and start command line logging.
        """
        # Top-level log setup.
        self.logger = logging.getLogger("data exchange") 
        if self._log_level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif self._log_level == 'INFO':
            self.logger.setLevel(logging.INFO) 
        elif self._log_level == 'WARN':
            self.logger.setLevel(logging.WARN)
        elif self._log_level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif self._log_level == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        
        # Terminal stream log.
        ch = logging.StreamHandler()
        if self._log_level == 'DEBUG':
            ch.setLevel(logging.DEBUG)
        elif self._log_level == 'INFO':
            ch.setLevel(logging.INFO) 
        elif self._log_level == 'WARN':
            ch.setLevel(logging.WARN)
        elif self._log_level == 'WARNING':
            ch.setLevel(logging.WARNING)
        elif self._log_level == 'ERROR':
            ch.setLevel(logging.ERROR)
        
        # Show date and time.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
            
        # Update logger.
        if not len(self.logger.handlers): # For fist time create handlers.
            self.logger.addHandler(ch)
