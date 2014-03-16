# -*- coding: utf-8 -*-
# file_name: data_convert.py
import numpy as np
import os
import h5py
from file_types import Tiff, Hdf4, Hdf5, Txrm, Xrm, Spe, Esrf, Tiffc, Netcdf
from data_exchange import DataExchangeFile, DataExchangeEntry

import logging
logger = logging.getLogger("data_exchange")

class Convert():
    def __init__(self, data=None, data_white=None, data_dark=None,
                 theta=None, log='INFO'):
        
        self.data = data
        self.data_white = data_white
        self.data_dark = data_dark
        self.theta = theta

        # Logging init.
        self._log_level = str(log).upper()
        self._init_log()

        # Prepare logging file.
        self._set_log_file()

        logger.debug("Data Exchange initialization [ok]")
    
    def series_of_images(self, file_name,
                projections_start=0,
                projections_end=None,
                projections_step=1,
                projections_angle_range=180,
                slices_start=0,
                slices_end=None,
                slices_step=1,
                white_file_name=None,
                white_start=0,
                white_end=None,
                white_step=1,
                dark_file_name=None,
                dark_start=0,
                dark_end=None,
                dark_step=1,
                projections_digits=4,
                white_digits=None,
                dark_digits=None,
                projections_zeros=True,
                white_zeros=True,
                dark_zeros=True,
                dtype='uint16',
                data_type='tiff',
                hdf5_file_name='dummy',
                sample_name=None,
                log='INFO'):

        """Read a series of HDF-4 or TIFF single images or a series of spe or netCDF stack images.

        Parameters
        ----------
        file_name : str
            Base name of the input HDF-4 or TIFF files.
            For example if the projections names are /local/data/test_XXXX.hdf
            file_name is /local/data/test_.hdf
            
        hdf5_file_name : str
            HDF5/data exchange file name

        projections_start, projections_end, projections_step : scalar, optional
            start and end index for the projection Tiff files to load. Use step define a stride.

        slices_start, slices_end, slices_step : scalar, optional
            start and end pixel of the projection image to load along the rotation axis. Use step define a stride.

        white_file_name : str
            Base name of the white field input HDF-4 or TIFF files: string optional.
            For example if the white field names are /local/data/test_bg_XXXX.hdf
            file_name is /local/data/test_bg_.hdf
            if omitted white_file_name = file_name.

        white_start, white_end : scalar, optional
            start and end index for the white field Tiff files to load. Use step define a stride.

        dark_file_name : str
            Base name of the dark field input HDF-4 or TIFF files: string optinal.
            For example if the white field names are /local/data/test_dk_XXXX.hdf
            file_name is /local/data/test_dk_.hdf
            if omitted dark_file_name = file_name.

        dark_start, dark_end : scalar, optional
            start and end index for the dark field Tiff files to load. Use step define a stride.

        projections_digits, white_digits, dark_digits : scalar, optional
            Number of projections_digits used for file indexing.
            For example if 4: test_XXXX.hdf

        projections_zeros, white_zeros, dark_zeros : bool, optional
            If ``True`` assumes all indexing uses four projections_digits
            (0001, 0002, ..., 9999). If ``False`` omits projections_zeros in
            indexing (1, 2, ..., 9999)

        dtype : str, optional
            Corresponding Numpy data type of the HDF-4 or TIFF file.

        data_type : str, optional
            supported options are:
                    hdf4: HDF-4 files used on old detector at APS 2-BM
                    compressed_tiff: tiff files used at elettra 
                    tiff: uncompressed regualar tiff files
                    spe: spe data from APS 13-BM
                    nc: netCDF data from 13-BM

        Returns
        -------
        inputData : list of hdf files contating projections, white and dark images

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """
        
        # Initialize Data Exchange file extension to false.
        hdf5_file_extension = False
        
        # Check inputs.
        if projections_end == None:
            logger.error("projections_end not defined.")
            return

        if white_end == None:
            logger.info("white range not defined.")

        if dark_end == None:
            logger.info("dark range not defined. ")

        if white_digits == None:
                white_digits = projections_digits
                
        if dark_digits == None:
                dark_digits = projections_digits

        logger.info("###############################################")
        logger.info("####      read series of [%s] images      ####", data_type)
        logger.info("###############################################")
        logger.info("projections file name= [%s]", file_name)
        logger.info("projections start [%d]", projections_start)
        logger.info("projections end [%d]", projections_end)
        logger.info("projections step [%d]", projections_step)
        logger.info("projections angle range [%d]", projections_angle_range)
        logger.info("white start [%d]", white_start)
        logger.info("white end [%d]", white_end)
        logger.info("white step [%d]", white_step)
        logger.info("dark start [%d]", dark_start)
        logger.info("dark end [%d]", dark_end)
        logger.info("dark step [%d]", dark_step)
        logger.info("projections digits [%d]", projections_digits)
        logger.info("white digits [%d]", white_digits)
        logger.info("dark digits [%d]", dark_digits)
        logger.info("projections zeros [%d]", projections_zeros)
        logger.info("white zeros [%d]", white_zeros)
        logger.info("dark zeros [%d]", dark_zeros)
        logger.info("dtype [%s]", dtype)
        logger.info("data type [%s]", data_type)
        logger.info("hdf5 file name [%s]", hdf5_file_name)
        logger.info("sample name [%s]", sample_name)
        logger.info("log [%s]", log)
        logger.info("Does the HDF file exist?  [%s]", os.path.isfile(hdf5_file_name))
        logger.info("#########################################")

        if os.path.isfile(hdf5_file_name):
            logger.info("Data Exchange file [%s] already exists. Nothing to do!", hdf5_file_name)
            logger.info("Please use the Data Exchange reader instead")

        else:
            # Read the series of files and load them in self.data, self.data_white, self.data_dark
            logger.info("Default projection file name white set [%s]", file_name)
            
            # Set default prefix for white and dark.
            if white_file_name == None:
                white_file_name = file_name
                logger.info("Default white file name set [%s]", white_file_name)
            if dark_file_name == None:
                dark_file_name = file_name
                logger.info("Default dark file name  set [%s]", dark_file_name)

            logger.info("File Name Projections = [%s]", file_name)
            logger.info("File Name White = [%s]", white_file_name)
            logger.info("File Name Dark = [%s]", dark_file_name)

            # Set default digits.
            if white_digits == None:
                white_digits = projections_digits
                logger.info("White digits = [%s]", white_digits)
            if dark_digits == None:
                dark_digits = projections_digits
                logger.info("Dark digits = [%s]", dark_digits)

            if (data_type is 'hdf4'):
                if file_name.endswith('h4') or \
                   file_name.endswith('hdf'):
                    dataFile = file_name.split('.')[-2]
                    dataExtension = file_name.split('.')[-1]
                if white_file_name.endswith('h4') or \
                   white_file_name.endswith('hdf'):
                    dataFileWhite = white_file_name.split('.')[-2]
                    dataExtensionWhite = white_file_name.split('.')[-1]
                if dark_file_name.endswith('h4') or \
                   dark_file_name.endswith('hdf'):
                    dataFileDark = dark_file_name.split('.')[-2]
                    dataExtensionDark = dark_file_name.split('.')[-1]

            elif (data_type is 'spe'):
                if file_name.endswith('SPE') or \
                   file_name.endswith('spe'):
                    dataFile = file_name.split('.')[-2]
                    dataExtension = file_name.split('.')[-1]
                if white_file_name.endswith('SPE') or \
                   white_file_name.endswith('spe'):
                    dataFileWhite = white_file_name.split('.')[-2]
                    dataExtensionWhite = white_file_name.split('.')[-1]
                if dark_file_name.endswith('SPE') or \
                   dark_file_name.endswith('spe'):
                    dataFileDark = dark_file_name.split('.')[-2]
                    dataExtensionDark = dark_file_name.split('.')[-1]

            elif (data_type is 'nc'):
                if file_name.endswith('NC') or \
                   file_name.endswith('nc'):
                    dataFile = file_name.split('.')[-2]
                    dataExtension = file_name.split('.')[-1]
                if white_file_name.endswith('NC') or \
                   white_file_name.endswith('nc'):
                    dataFileWhite = white_file_name.split('.')[-2]
                    dataExtensionWhite = white_file_name.split('.')[-1]
                if dark_file_name.endswith('NC') or \
                   dark_file_name.endswith('nc'):
                    dataFileDark = dark_file_name.split('.')[-2]
                    dataExtensionDark = dark_file_name.split('.')[-1]

            elif (data_type is 'tiff'):
                if file_name.endswith('tif') or \
                   file_name.endswith('tiff'):
                    dataFile = file_name.split('.')[-2]
                    dataExtension = file_name.split('.')[-1]
                if white_file_name.endswith('tif') or \
                   white_file_name.endswith('tiff'):
                    dataFileWhite = white_file_name.split('.')[-2]
                    dataExtensionWhite = white_file_name.split('.')[-1]
                if dark_file_name.endswith('tif') or \
                   dark_file_name.endswith('tiff'):
                    dataFileDark = dark_file_name.split('.')[-2]
                    dataExtensionDark = dark_file_name.split('.')[-1]
            

            projections_file_index = ["" for x in range(projections_digits)]

            for m in range(projections_digits):
                if projections_zeros is True:
                   projections_file_index[m] = '0' * (projections_digits - m - 1)

                elif projections_zeros is False:
                   projections_file_index[m] = ''

            white_file_index = ["" for x in range(white_digits)]
            for m in range(white_digits):
                if white_zeros is True:
                    white_file_index[m] = '0' * (white_digits - m - 1)

                elif white_zeros is False:
                    white_file_index[m] = ''

            dark_file_index = ["" for x in range(dark_digits)]
            for m in range(dark_digits):
                if dark_zeros is True:
                    dark_file_index[m] = '0' * (dark_digits - m - 1)

                elif dark_zeros is False:
                    dark_file_index[m] = ''
                   
            # Reading projections.
            ind = range(projections_start, projections_end, projections_step)
            #logger.info("projections: Start = [%d], End = [%d], Step = [%d]", projections_start, projections_end, projections_step)

            for m in range(len(ind)):
                for n in range(projections_digits):
                    #logger.info("n = [%d], ind[m] [%d] < [%d]", n, ind[m], np.power(10, n + 1))
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFile + projections_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info("Generating projection file names: [%s]", fileName)
                        break

                if os.path.isfile(fileName):
                    logger.info("Reading projection file: [%s]", os.path.realpath(fileName))
                    logger.info("data type: [%s]", data_type)

                    if (data_type is 'hdf4'):
                        f = Hdf4()
                        tmpdata = f.read(fileName,
                                         x_start=slices_start,
                                         x_end=slices_end,
                                         x_step=slices_step,
                                         array_name = 'data'
                                         )

                    elif (data_type is 'compressed_tiff'):
                        f = Tiffc()
                        tmpdata = f.read(fileName,
                                         x_start=slices_start,
                                         x_end=slices_end,
                                         x_step=slices_step,
                                         dtype=dtype
                                         )

                    elif (data_type is 'spe'):
                        f = Spe()
                        tmpdata = f.read(fileName)

                    elif (data_type is 'nc'):
                        f = Netcdf()
                        tmpdata = f.read(fileName)

                    elif (data_type is 'tiff'):
                        f = Tiff()
                        tmpdata = f.read(fileName,
                                         x_start=slices_start,
                                         x_end=slices_end,
                                         x_step=slices_step,
                                         dtype=dtype
                                         )

                    if ((data_type is 'tiff') or (data_type is 'compressed_tiff') or (data_type is 'hdf4')):
                        if m == 0: # Get resolution once.
                            inputData = np.empty((len(ind),
                                                  tmpdata.shape[0],
                                                  tmpdata.shape[1]),
                                                  dtype=dtype
                                                  )
                        inputData[m, :, :] = tmpdata

                    if ((data_type is 'spe') or (data_type is 'nc')):
                        if m == 0: # Get resolution once.
                            inputData = np.vstack([tmpdata])
                        else:
                            inputData = np.concatenate((inputData, tmpdata), axis=0)

            if len(ind) > 0:
                self.data = inputData

            # Reading white fields.
            ind = range(0,0,1)
            if white_end != None:
                ind = range(white_start, white_end, white_step)
                logger.info("white: Start = [%d], End = [%d], Step = [%d]", white_start, white_end, white_step)
                
                for m in range(len(ind)):
                    for n in range(white_digits):
                        logger.info("n = [%d], ind[m] [%d] < [%d]", n, ind[m], np.power(10, n + 1))
                        if ind[m] < np.power(10, n + 1):
                            fileName = dataFileWhite + white_file_index[n] + str(ind[m]) + '.' + dataExtension
                            logger.info("Generating white file names: [%s]", fileName)
                            break

                    if os.path.isfile(fileName):
                        logger.info("Reading white file: [%s]", os.path.realpath(fileName))
                        logger.info("data type: [%s]", data_type)

                        if (data_type is 'hdf4'):
                            f = Hdf4()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             array_name = 'data'
                                             )
                        elif (data_type is 'compressed_tiff'):
                            f = Tiffc()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             dtype=dtype
                                             )

                        elif (data_type is 'spe'):
                            f = Spe()
                            tmpdata = f.read(fileName)

                        elif (data_type is 'nc'):
                            f = Netcdf()
                            tmpdata = f.read(fileName)


                        elif (data_type is 'tiff'):
                            f = Tiff()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             dtype=dtype
                                             )

                        if ((data_type is 'tiff') or (data_type is 'compressed_tiff') or (data_type is 'hdf4')):
                            if m == 0: # Get resolution once.

                                inputData = np.empty((len(ind),
                                                     tmpdata.shape[0],
                                                     tmpdata.shape[1]),
                                                     dtype=dtype
                                                     )
                            inputData[m, :, :] = tmpdata

                        if ((data_type is 'spe') or (data_type is 'nc')):
                            if m == 0: # Get resolution once.
                                inputData = np.vstack([tmpdata])
                            else:
                                inputData = np.concatenate((inputData, tmpdata), axis=0)
            if len(ind) > 0:
                self.data_white = inputData
            else:
                # Fabricate one white field
                nz, ny, nx = np.shape(self.data)

            # Reading dark fields.
            ind = range(0,0,1)
            if dark_end != None:
                ind = range(dark_start, dark_end, dark_step)
                logger.info("dark: Start = [%d], End = [%d], Step = [%d]", dark_start, dark_end, dark_step)
                
                for m in range(len(ind)):
                    for n in range(dark_digits):
                        logger.info("n = [%d], ind[m] [%d] < [%d]", n, ind[m], np.power(10, n + 1))
                        if ind[m] < np.power(10, n + 1):
                            fileName = dataFileDark + dark_file_index[n] + str(ind[m]) + '.' + dataExtension
                            logger.info("Generating dark file names: [%s]", fileName)
                            break

                    if os.path.isfile(fileName):
                        logger.info("Reading dark file: [%s]", os.path.realpath(fileName))
                        logger.info("data type: [%s]", data_type)

                        if (data_type is 'hdf4'):
                            f = Hdf4()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             array_name = 'data'
                                             )

                        elif (data_type is 'compressed_tiff'):
                            f = Tiffc()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             dtype=dtype
                                             )

                        elif (data_type is 'spe'):
                            f = Spe()
                            tmpdata = f.read(fileName)

                        elif (data_type is 'nc'):
                            f = Netcdf()
                            tmpdata = f.read(fileName)

                        elif (data_type is 'tiff'):
                            f = Tiff()
                            tmpdata = f.read(fileName,
                                             x_start=slices_start,
                                             x_end=slices_end,
                                             x_step=slices_step,
                                             dtype=dtype
                                             )

                        if ((data_type is 'tiff') or (data_type is 'compressed_tiff') or (data_type is 'hdf4')):
                            if m == 0: # Get resolution once.
                                inputData = np.empty((len(ind),
                                                      tmpdata.shape[0],
                                                      tmpdata.shape[1]),
                                                      dtype=dtype
                                                      )
                            inputData[m, :, :] = tmpdata

                        if ((data_type is 'spe') or (data_type is 'nc')):
                            if m == 0: # Get resolution once.
                                inputData = np.vstack([tmpdata])
                            else:
                                inputData = np.concatenate((inputData, tmpdata), axis=0)
            if len(ind) > 0:
                self.data_dark = inputData
            else:
                # Fabricate one dark field
                nz, ny, nx = np.shape(self.data)
                self.data_dark = np.ones((1, ny, nx))
                
            if ((data_type is 'tiff') or (data_type is 'compressed_tiff') or (data_type is 'hdf4')):
                # Fabricate theta values.
                z = np.arange(projections_end - projections_start);
                    
                # Fabricate theta values
                self.theta = (z * float(projections_angle_range) / (len(z) - 1))

            # Getting ready to save the Data Exchange file
            if (hdf5_file_name != 'dummy'):
                logger.info("Data Exchange file is set to [%s]", hdf5_file_name)

                # Get the file_name in lower case.
                lFn = hdf5_file_name.lower()

                # Split the string with the delimeter '.'
                end = lFn.split('.')
                logger.info(end)
                
                # If the string has an extension.
                if len(end) > 1:
                    # Check.
                    if end[len(end) - 1] == 'h5' or end[len(end) - 1] == 'hdf':
                        hdf5_file_extension = True
                        logger.info("HDF5 file extension is .h5 or .hdf")
                    else:
                        hdf5_file_extension = False
                        logger.warning("HDF5 file saved with an extension that is not .h5 or .hdf")

                # Create new folder.
                dirPath = os.path.dirname(hdf5_file_name)
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)

                # Write the Data Exchange HDF5 file.
                # Open DataExchange file
                f = DataExchangeFile(hdf5_file_name, mode='w') 

                logger.info("Creating Data Exchange File [%s]", hdf5_file_name)

                # Create core HDF5 dataset in exchange group for projections_theta_range
                # deep stack of x,y images /exchange/data
                logger.info("Adding projections to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                if ((data_type is 'tiff') or (data_type is 'compressed_tiff') or (data_type is 'hdf4')):
                    f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
                logger.info("Adding dark fields to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data_dark={'value': self.data_dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                logger.info("Adding white fields to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data_white={'value': self.data_white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
                if (sample_name == None):
                    sample_name = end[0]
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 file name'}))
                    logger.info("Sample name assigned by HDF5 converter using the file name [%s]", end[0])
                else:
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                    logger.info("Sample name assigned by user")
                logger.info("Sample name = [%s]", sample_name)
                                   
                logger.info("Closing Data Exchange File [%s]", hdf5_file_name)
                f.close()
                logger.info("DONE!!!!. Created Data Exchange File [%s]", hdf5_file_name)
            else:
                logger.warning("Data Exchange file name was not set => series of files are in memory only and passed to self.data, self.data_dark, self.data_white")

    def nexus(self, file_name,
                  hdf5_file_name,
                  projections_start=0,
                  projections_end=None,
                  projections_step=1,
                  slices_start=0,
                  slices_end=None,
                  slices_step=1,
                  pixels_start=0,
                  pixels_end=None,
                  pixels_step=1,
                  white_start=0,
                  white_end=None,
                  dark_start=0,
                  dark_end=None,
                  array_name='entry/instrument/detector/data',
                  sample_name=None,
                  dtype='float32'):
        """ Read Data Exchange HDF5 file.

        Parameters
        ----------
        file_name : str
            Input file.

        projections_start, projections_end, projections_step : scalar, optional
            Values of the start, end and step of the projections to
            be used for slicing for the whole ndarray.

        slices_start, slices_end, slices_step : scalar, optional
            Values of the start, end and step of the slices to
            be used for slicing for the whole ndarray.

        pixels_start, pixels_end, pixels_step : scalar, optional
            Values of the start, end and step of the pixels to
            be used for slicing for the whole ndarray.

        white_start, white_end : scalar, optional
            Values of the start, end and step of the
            slicing for the whole white field shots.

        dark_start, dark_end : scalar, optional
            Values of the start, end and step of the
            slicing for the whole dark field shots.

        dtype : str, optional
            Desired output data type.
        """
        
        # Check inputs.
        if file_name == None:
            logger.error("file_name not defined.")
            return
        if projections_end == None:
            logger.error("projections_end not defined.")
            return
        if slices_end == None:
            logger.error("slices_end not defined.")
            return
        if pixels_end == None:
            logger.error("pixels_end not defined.")
            return
        if white_end == None:
            logger.error("white_end not defined.")
            return
        if dark_end == None:
            logger.error("dark_end not defined.")
            return
        if sample_name == None:
            logger.error("sanple_name not defined.")
            return
        
        print "Reading NeXus file ..."
        self.file_name = file_name

        # Initialize f to null.
        f = None

        # Get the file_name in lower case.
        lFn = file_name.lower()

        # Split the string with the delimeter '.'
        end = lFn.split('.')

        # If the string has an extension.
        if len(end) > 1:
            # Check.
            if end[len(end) - 1] == 'h5' or end[len(end) - 1] == 'hdf':
                f = Hdf5()

        # If f != None the call read on it.
        if not f == None:
            # Read data from exchange group.
            self.data = f.read(file_name,
                                array_name=array_name,
                                x_start=projections_start,
                                x_end=projections_end,
                                x_step=projections_step,
                                y_start=slices_start,
                                y_end=slices_end,
                                y_step=slices_step,
                                z_start=pixels_start,
                                z_end=pixels_end,
                                z_step=pixels_step).astype(dtype)

            # Read white field data from exchange group.
            #print white_start, white_end, slices_start, slices_end
            self.data_white = f.read(file_name,
                                array_name=array_name,
                                x_start=white_start,
                                x_end=white_end,
                                y_start=slices_start,
                                y_end=slices_end,
                                y_step=slices_step,
                                z_start=pixels_start,
                                z_end=pixels_end,
                                z_step=pixels_step).astype(dtype)

            # Read dark field data from exchange group.
            self.data_dark = f.read(file_name,
                                array_name=array_name,
                                x_start=dark_start,
                                x_end=dark_end,
                                y_start=slices_start,
                                y_end=slices_end,
                                y_step=slices_step,
                                z_start=pixels_start,
                                z_end=pixels_end,
                                z_step=pixels_step).astype(dtype)

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            logger.info("Writing the HDF5 file")
            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.data_dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.data_white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = [%s]", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 file name'}))
                logger.info("Assigned default file name: [%s]", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")                    
            
            f.close()

        else:
            print 'Unsupported file.'

    def stack(self, file_name,
                projections_data_type='txrm',
                white_file_name='',
                white_data_type='xrm',
                dark_file_name='',
                dark_data_type='xrm',
                hdf5_file_name='dummy',
                sample_name=None,
                log='INFO'):
        """Read a stack of tomographic data consisting of up to 3 files.

            Supported formats:
            
            Data Exchange: one single HDF5 file follwoing the definition from http://www.aps.anl.gov/DataExchange/
                NOT COMPLETED YET
            
            X-radia data:
                txrm: one mandatory file, containing the projections
                xrm: two optional files contating white and dark images

            ESRF ID-19 data:
                ESRF tomography data consists of 3 edf files each containing
                staks of images. The comverter requires:
                edf: one mandatory file, containing the projections
                edf: two optional files contating white and dark images

        Parameters
        ----------
        file_name : str
            Name of the txrm/edf file containing the projections.
            
        hdf5_file_name : str
            HDF5/data exchange file name

        white_file_name, dark_file_name : str, optional
            Name of the xrm/edf fileS containing the white and dark images

        projection_data_type, white_data_type, dark_data_type : str, optional

        Returns
        -------
        inputData : list of hdf files contating projections, white and dark images

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """
        # Check inputs.
        if sample_name == None:
            logger.error("sanple_name not defined.")
            return
        
        # Initialize Data Exchange file extension to false.
        hdf5_file_extension = False

        logger.info("###############################################")
        logger.info("####      read stack of [%s] images       ####", projections_data_type)
        logger.info("###############################################")
        logger.info("projections file name= [%s]", file_name)
        logger.info("projections data type [%s]", projections_data_type)
        logger.info("white file name [%s]", white_file_name)
        logger.info("white data type [%s]", white_data_type)
        logger.info("dark file name [%s]", dark_file_name)
        logger.info("dark data type [%s]", dark_data_type)
        logger.info("hdf5 file name [%s]", hdf5_file_name)
        logger.info("sample name [%s]", sample_name)
        logger.info("log [%s]", log)
        logger.info("Does the HDF file exist?  [%s]", os.path.isfile(hdf5_file_name))
        logger.info("#########################################")

        if os.path.isfile(hdf5_file_name):
                logger.info("Data Exchange file [%s] already exists. Nothing to convert!", hdf5_file_name)
                logger.info("Reading the Data Exchange")
                # ADD DATA EXCHANGE READER CALL HERE

        else:
            # Read the series of files and load them in self.data, self.data_white, self.data_dark

            logger.info("File Name Projections = [%s]", file_name)
            logger.info("File Name White = [%s]", white_file_name)
            logger.info("File Name Dark = [%s]", dark_file_name)

            if os.path.isfile(file_name):
                logger.info("Reading projections file: [%s]", os.path.realpath(file_name))
                logger.info("data type: [%s]", projections_data_type)
                if (projections_data_type is 'txrm'):
                    f = Txrm()
                    tmpdata = f.read(file_name)
                    self.data = tmpdata
                if (projections_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(file_name)
                    self.data = tmpdata
                
            if os.path.isfile(white_file_name):
                logger.info("Reading white file: [%s]", os.path.realpath(white_file_name))
                logger.info("data type: [%s]", white_data_type)
                if (white_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(white_file_name)
                    self.data_white = tmpdata
                if (white_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(white_file_name)
                    self.data_white = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.data_white = np.ones((nx,ny,1))

            if os.path.isfile(dark_file_name):
                logger.info("Reading dark file: [%s]", os.path.realpath(dark_file_name))
                logger.info("data type: [%s]", dark_data_type)
                if (dark_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(dark_file_name)
                    self.data_dark = tmpdata
                if (dark_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(dark_file_name)
                    self.data_dark = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.data_dark = np.zeros((nx,ny,1))

            # Getting ready to save the Data Exchange file

            if (hdf5_file_name != 'dummy'):
                logger.info("Data Exchange file is set to [%s]", hdf5_file_name)

                # Get the file_name in lower case.
                lFn = hdf5_file_name.lower()

                # Split the string with the delimeter '.'
                end = lFn.split('.')
                logger.info(end)
                # If the string has an extension.
                if len(end) > 1:
                    # Check.
                    if end[len(end) - 1] == 'h5' or end[len(end) - 1] == 'hdf':
                        hdf5_file_extension = True
                        logger.info("HDF5 file extension is .h5 or .hdf")
                    else:
                        hdf5_file_extension = False
                        logger.warning("HDF5 file saved with an extension that is not .h5 or .hdf")

                # Create new folder.
                dirPath = os.path.dirname(hdf5_file_name)
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)

                # Write the Data Exchange HDF5 file.
                # Open DataExchange file
                f = DataExchangeFile(hdf5_file_name, mode='w') 

                logger.info("Creating Data Exchange File [%s]", hdf5_file_name)

                # Create core HDF5 dataset in exchange group for projections_theta_range
                # deep stack of x,y images /exchange/data
                logger.info("Adding projections to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
                logger.info("Adding dark fields to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data_dark={'value': self.data_dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                logger.info("Adding white fields to  Data Exchange File [%s]", hdf5_file_name)
                f.add_entry( DataExchangeEntry.data(data_white={'value': self.data_white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
                f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
                if (sample_name == None):
                    sample_name = end[0]
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 file name'}))
                    logger.info("Sample name assigned by HDF5 converter using the file name [%s]", end[0])
                else:
                    f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                    logger.info("Sample name assigned by user")
                logger.info("Sample name = [%s]", sample_name)
                                   
                logger.info("Closing Data Exchange File [%s]", hdf5_file_name)
                f.close()
                logger.info("DONE!!!!. Created Data Exchange File [%s]", hdf5_file_name)
            else:
                logger.warning("Data Exchange file name was not set => read series of files in memory only.")

    def _init_log(self):
        # Top-level log setup.
        logger.setLevel(logging.DEBUG)
        
        # Terminal stram log.
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
        logger.addHandler(ch)
        
    def _set_log_file(self):
        log_name = "data_exchange.log"
        
        # File log.
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.DEBUG)
            
        # Show date and time.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Update logger.
        logger.addHandler(fh)

        logger.info("logger file [ok]")


