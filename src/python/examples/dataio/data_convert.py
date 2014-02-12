# -*- coding: utf-8 -*-
# file_name: data_convert.py
import numpy as np
import os
import h5py
from dataio.file_types import Tiff, Hdf4, Hdf5, Txrm, Xrm, Spe, Esrf
from data_exchange import DataExchangeFile, DataExchangeEntry
import dataio.data_spe as spe
import logging
logger = logging.getLogger(__name__)

class Convert():
    def __init__(self, data=None, white=None, dark=None,
                 center=None, angles=None):
        self.data = data
        self.white = white
        self.dark = dark
        self.center = center
        self.theta = angles
    
    def series_of_images(self, file_name,
                hdf5_file_name,
                projections_start=0,
                projections_end=0,
                projections_step=1,
                projections_angle_range=180,
                slices_start=None,
                slices_end=None,
                slices_step=None,
                pixels_start=None,
                pixels_end=None,
                pixels_step=None,
                white_file_name=None,
                white_start=0,
                white_end=0,
                white_step=1,
                dark_file_name=None,
                dark_start=0,
                dark_end=0,
                dark_step=1,
                projections_digits=4,
                white_digits=-1,
                dark_digits=-1,
                zeros=True,
                dtype='uint16',
                data_type='tiff',
                sample_name=None,
                verbose=True):
        """Read a stack of HDF-4 or TIFF files in a folder.

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

        pixels_start, pixels_end, pixels_step : not used yet.

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

        projections_digits : scalar, optional
            Number of projections_digits used for file indexing.
            For example if 4: test_XXXX.hdf

        zeros : bool, optional
            If ``True`` assumes all indexing uses four projections_digits
            (0001, 0002, ..., 9999). If ``False`` omits zeros in
            indexing (1, 2, ..., 9999)

        dtype : str, optional
            Corresponding Numpy data type of the HDF-4 or TIFF file.

        data_type : str, optional
            if 'hdf4q m    ' will convert HDF-4 files (old 2-BM), deafult is 'tiff'

        Returns
        -------
        inputData : list of hdf files contating projections, white and dark images

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """

        # Initialize f to null.
        hdf5_file_extension = False

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
                logger.info("HDF file extension is .h5 or .hdf")
            else:
                hdf5_file_extension = False
                logger.info("HDF file extension must be .h5 or .hdf")
               
        # If the extension is correct and the file does not exists then convert
        if (hdf5_file_extension and (os.path.isfile(hdf5_file_name) == False)):
            # Create new folder.
            dirPath = os.path.dirname(hdf5_file_name)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            # Prepare hdf file names to be read.
            if white_file_name == None:
                    white_file_name = file_name
                    logger.info("File Name White = %s", white_file_name)
            if dark_file_name == None:
                    dark_file_name = file_name
                    logger.info("File Name Dark = %s", dark_file_name)

            logger.info("File Name Projections = %s", file_name)
            logger.info("File Name White = %s", white_file_name)
            logger.info("File Name Dark = %s", dark_file_name)

            # Set default digits.
            if white_digits == -1:
                    white_digits = projections_digits
                    logger.info("White digits = %s", white_digits)
            if dark_digits == -1:
                    dark_digits = projections_digits
                    logger.info("Dark digits= %s", dark_digits)

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
            else:
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
                if zeros is True:
                   projections_file_index[m] = '0' * (projections_digits - m - 1)

                elif zeros is False:
                   projections_file_index[m] = ''

            white_file_index = ["" for x in range(white_digits)]
            for m in range(white_digits):
                if zeros is True:
                   white_file_index[m] = '0' * (white_digits - m - 1)

                elif zeros is False:
                   white_file_index[m] = ''

            dark_file_index = ["" for x in range(dark_digits)]
            for m in range(dark_digits):
                if zeros is True:
                   dark_file_index[m] = '0' * (dark_digits - m - 1)

                elif zeros is False:
                   dark_file_index[m] = ''
                   
            # Reading projections.
            ind = range(projections_start, projections_end)
            logger.info("projections: Start = %d, End = %d, Step = %d", projections_start, projections_end, projections_step)
            for m in range(len(ind)):
                for n in range(projections_digits):
                    logger.info("n = %d, ind[m] %d < %d", n, ind[m], np.power(10, n + 1))
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFile + projections_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info("Generating file names: %s", fileName)
                        break

                if os.path.isfile(fileName):
                    logger.info("Reading projection file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'hdf4'):
                        f = Hdf4()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            array_name = 'data'
                                         )
                    else:
                        f = Tiff()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            dtype=dtype
                                         )
                    if m == 0: # Get resolution once.
                        inputData = np.empty((projections_end-projections_start,
                                            tmpdata.shape[0],
                                            tmpdata.shape[1]),
                                            dtype=dtype
                                    )
                    inputData[m, :, :] = tmpdata
            if len(ind) > 0:
                self.data = inputData

            # Reading white fields.
            ind = range(white_start, white_end, white_step)
            logger.info("white: Start = %d, End = %d, Step = %d", white_start, white_end, white_step)
            for m in range(len(ind)):
                for n in range(white_digits):
                    logger.info("n = %d, ind[m] %d < %d", n, ind[m], np.power(10, n + 1))
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFileWhite + white_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info(fileName)
                        break

                if os.path.isfile(fileName):
                    logger.info("Reading white file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'hdf4'):
                        f = Hdf4()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            array_name = 'data'
                                         )
                    else:
                        f = Tiff()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            dtype=dtype
                                         )
                    if m == 0: # Get resolution once.
                        inputData = np.empty(((white_end - white_start)/white_step + 1,
                                            tmpdata.shape[0],
                                            tmpdata.shape[1]),
                                            dtype=dtype
                                        )
                    inputData[m, :, :] = tmpdata
            if len(ind) > 0:
                self.white = inputData
                
            # Reading dark fields.
            ind = range(dark_start, dark_end, dark_step)
            logger.info("dark: Start = %d, End = %d, Step = %d", dark_start, dark_end, dark_step)
            for m in range(len(ind)):
                for n in range(dark_digits):
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFileDark + dark_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info(fileName)
                        break

                if os.path.isfile(fileName):
                    logger.info("Reading dark file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'hdf4'):
                        f = Hdf4()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            array_name = 'data'
                                         )
                    else:
                        f = Tiff()
                        tmpdata = f.read(fileName,
                                            x_start=slices_start,
                                            x_end=slices_end,
                                            x_step=slices_step,
                                            dtype=dtype
                                         )
                    if m == 0: # Get resolution once.
                        inputData = np.empty(((dark_end - dark_start),
                                            tmpdata.shape[0],
                                            tmpdata.shape[1]),
                                            dtype=dtype
                                        )
                    inputData[m, :, :] = tmpdata
            if len(ind) > 0:
                self.dark = inputData
                
            # Fabricate theta values.
            z = np.arange(projections_end - projections_start);
                
            # Fabricate theta values
            self.theta = (z * float(projections_angle_range) / (len(z) - 1))

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = %s", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 fine name'}))
                logger.info("Assigned default file name: %s", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")
                               
            f.close()
        else:
            if os.path.isfile(hdf5_file_name):
                print 'HDF5 already exists. Nothing to do ...'
            if (hdf5_file_extension == False):
                print "HDF file extension must be .h5 or .hdf"

    def x_radia(self, file_name,
                hdf5_file_name,
                projections_data_type='txrm',
                white_file_name='',
                white_data_type='xrm',
                dark_file_name='',
                dark_data_type='xrm',
                sample_name=None,
                verbose=True):
        """Read a stack xradia files. This consists of up to 3 files:
            txrm: one mandatory file, containing the projections
            xrm: two optional files contating white and dark images

        Parameters
        ----------
        file_name : str
            Name of the txrm file containing the projections.
            
        hdf5_file_name : str
            HDF5/data exchange file name

        white_file_name, dark_file_name : str, optional
            Name of the xrm fileS containing the white and dark images

        projection_data_type, white_data_type, dark_data_type : str, optional

        Returns
        -------
        inputData : list of hdf files contating projections, white and dark images

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """

        # Initialize f to null.
        hdf5_file_extension = False

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
                logger.info("HDF file extension is .h5 or .hdf")
            else:
                hdf5_file_extension = False
                logger.info("HDF file extension must be .h5 or .hdf")
                
        # If the extension is correct and the file does not exists then convert
        if (hdf5_file_extension and (os.path.isfile(hdf5_file_name) == False)):
            # Create new folder.
            dirPath = os.path.dirname(hdf5_file_name)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            logger.info("File Name Projections = %s", file_name)
            logger.info("File Name White = %s", white_file_name)
            logger.info("File Name Dark = %s", dark_file_name)

            if os.path.isfile(file_name):
                logger.info("Reading projections file: %s", os.path.realpath(file_name))
                logger.info("data type: %s", projections_data_type)
                if (projections_data_type is 'txrm'):
                    f = Txrm()
                    tmpdata = f.read(file_name)
                    self.data = tmpdata

            if os.path.isfile(white_file_name):
                logger.info("Reading white file: %s", os.path.realpath(white_file_name))
                logger.info("data type: %s", white_data_type)
                if (white_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(white_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.white = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.dark = np.ones((nx,ny,1))

            if os.path.isfile(dark_file_name):
                logger.info("Reading dark file: %s", os.path.realpath(dark_file_name))
                logger.info("data type: %s", dark_data_type)
                if (white_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(dark_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.dark = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.dark = np.zeros((nx,ny,1))

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            logger.info("Writing the HDF5 file")
            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = %s", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 fine name'}))
                logger.info("Assigned default file name: %s", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")
                                
            f.close()
        else:
            if os.path.isfile(hdf5_file_name):
                print 'HDF5 already exists. Nothing to do ...'
            if (hdf5_file_extension == False):
                print "HDF file extension must be .h5 or .hdf"

    def multiple_stack(self, file_name,
                hdf5_file_name,
                projections_start=0,
                projections_end=1,
                projections_step=1,
                white_file_name=None,
                white_start=0,
                white_end=0,
                white_step=1,
                dark_file_name=None,
                dark_start=0,
                dark_end=0,
                dark_step=1,
                projections_digits=4,
                white_digits=-1,
                dark_digits=-1,
                zeros=False,
                data_type='spe',
                sample_name=None,
                verbose=False):
        """Read a stack spe files. Each SPE file contains a stack of projections/white images

        Parameters
        ----------
        file_name : str
            Base name of the input SPE files.
            For example if the projection file names are /local/data/test_XXXX.SPE
            file_name is /local/data/test_.hdf
            
        projections_start, projections_end, projections_step : scalar, optional
            start and end index for the projection Tiff files to load. Use step define a stride.

        white_file_name : str
            Base name of the white field input SPE files: string optional.
            For example if the white field names are /local/data/test_bg_XXXX.SPE
            file_name is /local/data/test_bg_.SPE
            if omitted white_file_name = file_name.

        white_start, white_end, white_step : scalar, optional
            start and end index for the white field SPE files to load.
            white_step defines the stride.

        dark_file_name : str
            Base name of the dark field input SPE files: string optinal.
            For example if the white field names are /local/data/test_dk_XXXX.SPE
            file_name is /local/data/test_dk_.SPE
            if omitted dark_file_name = file_name.

        dark_start, dark_end, dark_step : scalar, optional
            start and end index for the dark field Tiff files to load. 
            dark_step defines the stride.

        projections_digits : scalar, optional
            Number of projections_digits used for file indexing.
            For example if 4: test_XXXX.hdf

        zeros : bool, optional
            If ``True`` assumes all indexing uses four projections_digits
            (0001, 0002, ..., 9999). If ``False`` omits zeros in
            indexing (1, 2, ..., 9999)

        data_type : str, optional
            Not used 
            
        hdf5_file_name : str
            HDF5/data exchange file name

        Returns
        -------

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """

        logger.info("Call to multiple_stack")
        # Initialize f to null.
        hdf5_file_extension = False

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
                logger.info("HDF file extension is .h5 or .hdf")
            else:
                hdf5_file_extension = False
                logger.info("HDF file extension must be .h5 or .hdf")
                
        # If the extension is correct and the file does not exists then convert
        if (hdf5_file_extension and (os.path.isfile(hdf5_file_name) == False)):
            # Create new folder.
            dirPath = os.path.dirname(hdf5_file_name)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            # Prepare hdf file names to be read.
            if white_file_name == None:
                    white_file_name = file_name
                    logger.info("File Name White = %s", white_file_name)
            if dark_file_name == None:
                    dark_file_name = file_name
                    logger.info("File Name Dark = %s", dark_file_name)

            logger.info("File Name Projections = %s", file_name)
            logger.info("File Name White = %s", white_file_name)
            logger.info("File Name Dark = %s", dark_file_name)

            # Set default digits.
            if white_digits == -1:
                    white_digits = projections_digits
                    logger.info("White digits = %s", white_digits)
            if dark_digits == -1:
                    dark_digits = projections_digits
                    logger.info("Dark digits= %s", dark_digits)

            if (data_type is 'spe'):
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

            projections_file_index = ["" for x in range(projections_digits)]
            for m in range(projections_digits):
                if zeros is True:
                   projections_file_index[m] = '0' * (projections_digits - m - 1)

                elif zeros is False:
                   projections_file_index[m] = ''

            white_file_index = ["" for x in range(white_digits)]
            for m in range(white_digits):
                if zeros is True:
                   white_file_index[m] = '0' * (white_digits - m - 1)

                elif zeros is False:
                   white_file_index[m] = ''

            dark_file_index = ["" for x in range(dark_digits)]
            for m in range(dark_digits):
                if zeros is True:
                   dark_file_index[m] = '0' * (dark_digits - m - 1)

                elif zeros is False:
                   dark_file_index[m] = ''

            # Reading projections.
            fileName = ''
            ind = range(projections_start, projections_end, projections_step)
            logger.info("projections: Start = %d, End = %d, Step = %d", projections_start, projections_end, projections_step)
            for m in range(len(ind)):
                for n in range(projections_digits):
                    logger.info("n = %d, ind[m] %d < %d", n, ind[m], np.power(10, n + 1))
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFile + projections_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info("Generating file names: %s", fileName)
                        break
                if os.path.isfile(fileName):
                    spe_data = spe.PrincetonSPEFile(fileName)
                    logger.info(spe_data)

                    logger.info("Reading projections file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'spe'):
                        f = Spe()
                        tmpdata = f.read(fileName)
                        logger.info("tmpData: %d, %d, %d", tmpdata.shape[0], tmpdata.shape[1], tmpdata.shape[2])  
                        if m == 0: # Get resolution once.
                            inputData = np.vstack([tmpdata])
                        else:
                            inputData = np.concatenate((inputData, tmpdata), axis=0)
                            logger.info("InputData: %d, %d, %d", inputData.shape[0], inputData.shape[1], inputData.shape[2])

            if len(ind) > 0:
                self.data = inputData
                logger.info("Done loading projections")
                logger.info("Data: %d, %d, %d", self.data.shape[0], self.data.shape[1], self.data.shape[2])  

            # Reading white.
            fileName = ''
            ind = range(white_start, white_end, white_step)
            logger.info("white: Start = %d, End = %d, Step = %d", white_start, white_end, white_step)
            for m in range(len(ind)):
                for n in range(white_digits):
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFile + white_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info("Generating file names: %s", fileName)
                        break
                if os.path.isfile(fileName):
                    spe_data = spe.PrincetonSPEFile(fileName)
                    logger.info(spe_data)

                    logger.info("Reading white file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'spe'):
                        f = Spe()
                        tmpdata = f.read(fileName)
                        logger.info("tmpData: %d, %d, %d", tmpdata.shape[0], tmpdata.shape[1], tmpdata.shape[2])  
                        if m == 0: # Get resolution once.
                            inputData = np.vstack([tmpdata])
                        else:
                            inputData = np.concatenate((inputData, tmpdata), axis=0)
                            logger.info("InputData: %d, %d, %d", inputData.shape[0], inputData.shape[1], inputData.shape[2])

            if len(ind) > 0:
                self.white = inputData
                logger.info("Done loading white")
                logger.info("WhiteData: %d, %d, %d", self.white.shape[0], self.white.shape[1], self.white.shape[2])
            else:
                nx, ny, nz = np.shape(self.data)
                self.white = np.ones((1, ny, nx))

            # Reading dark.
            fileName = ''
            ind = range(dark_start, dark_end, dark_step)
            logger.info("dark: Start = %d, End = %d, Step = %d", dark_start, dark_end, dark_step)
            for m in range(len(ind)):
                for n in range(dark_digits):
                    logger.info("n = %d, ind[m] %d < %d", n, ind[m], np.power(10, n + 1))
                    if ind[m] < np.power(10, n + 1):
                        fileName = dataFile + dark_file_index[n] + str(ind[m]) + '.' + dataExtension
                        logger.info("Generating file names: %s", fileName)
                        break
                if os.path.isfile(fileName):
                    spe_data = spe.PrincetonSPEFile(fileName)
                    logger.info(spe_data)

                    logger.info("Reading dark file: %s", os.path.realpath(fileName))
                    logger.info("data type: %s", data_type)
                    if (data_type is 'spe'):
                        f = Spe()
                        tmpdata = f.read(fileName)
                        logger.info("tmpData: %d, %d, %d", tmpdata.shape[0], tmpdata.shape[1], tmpdata.shape[2])  
                        if m == 0: # Get resolution once.
                            inputData = np.vstack([tmpdata])
                        else:
                            inputData = np.concatenate((inputData, tmpdata), axis=0)
                            logger.info("InputData: %d, %d, %d", inputData.shape[0], inputData.shape[1], inputData.shape[2])

            if len(ind) > 0:
                self.dark = inputData
                logger.info("Done loading dark")
                logger.info(self.dark.shape[0], self.dark.shape[1], self.dark.shape[2])  
            else:
                nx, ny, nz = np.shape(self.data)
                self.dark = np.zeros((1, ny, nx))

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            logger.info("Writing the HDF5 file")
            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = %s", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 fine name'}))
                logger.info("Assigned default file name: %s", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")                    
            
            f.close()
        else:
            if os.path.isfile(hdf5_file_name):
                print 'HDF5 already exists. Nothing to do ...'
            if (hdf5_file_extension == False):
                print "HDF file extension must be .h5 or .hdf"

    def nexus(self, file_name,
                  hdf5_file_name,
                  projections_start=None,
                  projections_end=None,
                  projections_step=None,
                  slices_start=None,
                  slices_end=None,
                  slices_step=None,
                  pixels_start=None,
                  pixels_end=None,
                  pixels_step=None,
                  white_start=None,
                  white_end=None,
                  dark_start=None,
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
            print white_start, white_end, slices_start, slices_end
            self.white = f.read(file_name,
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
            self.dark = f.read(file_name,
                                array_name=array_name,
                                x_start=dark_start,
                                x_end=dark_end,
                                y_start=slices_start,
                                y_end=slices_end,
                                y_step=slices_step,
                                z_start=pixels_start,
                                z_end=pixels_end,
                                z_step=pixels_step).astype(dtype)

            # Assign the rotation center.
            self.center = self.data.shape[2] / 2

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            logger.info("Writing the HDF5 file")
            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = %s", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 fine name'}))
                logger.info("Assigned default file name: %s", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")                    
            
            f.close()

        else:
            print 'Unsupported file.'

    def stack(self, file_name,
                hdf5_file_name,
                projections_data_type='txrm',
                white_file_name='',
                white_data_type='xrm',
                dark_file_name='',
                dark_data_type='xrm',
                sample_name=None,
                verbose=True):
        """Read a stack xradia files. This consists of up to 3 files:
            txrm: one mandatory file, containing the projections
            xrm: two optional files contating white and dark images

        Parameters
        ----------
        file_name : str
            Name of the txrm file containing the projections.
            
        hdf5_file_name : str
            HDF5/data exchange file name

        white_file_name, dark_file_name : str, optional
            Name of the xrm fileS containing the white and dark images

        projection_data_type, white_data_type, dark_data_type : str, optional

        Returns
        -------
        inputData : list of hdf files contating projections, white and dark images

        Output : saves the data as HDF5 in hdf5_file_name

        .. See also:: http://docs.scipy.org/doc/numpy/user/basics.types.html
        """

        # Initialize f to null.
        hdf5_file_extension = False

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
                logger.info("HDF file extension is .h5 or .hdf")
            else:
                hdf5_file_extension = False
                logger.info("HDF file extension must be .h5 or .hdf")
                
        # If the extension is correct and the file does not exists then convert
        if (hdf5_file_extension and (os.path.isfile(hdf5_file_name) == False)):
            # Create new folder.
            dirPath = os.path.dirname(hdf5_file_name)
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

            logger.info("File Name Projections = %s", file_name)
            logger.info("File Name White = %s", white_file_name)
            logger.info("File Name Dark = %s", dark_file_name)

            if os.path.isfile(file_name):
                logger.info("Reading projections file: %s", os.path.realpath(file_name))
                logger.info("data type: %s", projections_data_type)
                if (projections_data_type is 'txrm'):
                    f = Txrm()
                    tmpdata = f.read(file_name)
                    self.data = tmpdata
                if (projections_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(file_name)
                    self.data = tmpdata
                
            if os.path.isfile(white_file_name):
                logger.info("Reading white file: %s", os.path.realpath(white_file_name))
                logger.info("data type: %s", white_data_type)
                if (white_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(white_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.white = tmpdata
                if (white_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(white_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.white = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.dark = np.ones((nx,ny,1))

            if os.path.isfile(dark_file_name):
                logger.info("Reading dark file: %s", os.path.realpath(dark_file_name))
                logger.info("data type: %s", dark_data_type)
                if (white_data_type is 'xrm'):
                    f = Xrm()
                    tmpdata = f.read(dark_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.dark = tmpdata
                if (white_data_type is 'edf'):
                    f = Esrf()
                    tmpdata = f.read(dark_file_name)
                    #inputData[m, :, :] = tmpdata
                    self.dark = tmpdata
            else:
                nx, ny, nz = np.shape(self.data)
                self.dark = np.zeros((nx,ny,1))

            # Write HDF5 file.
            # Open DataExchange file
            f = DataExchangeFile(hdf5_file_name, mode='w') 

            logger.info("Writing the HDF5 file")
            # Create core HDF5 dataset in exchange group for projections_theta_range
            # deep stack of x,y images /exchange/data
            f.add_entry( DataExchangeEntry.data(data={'value': self.data, 'units':'counts', 'description': 'transmission', 'axes':'theta:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(theta={'value': self.theta, 'units':'degrees'}))
            f.add_entry( DataExchangeEntry.data(data_dark={'value': self.dark, 'units':'counts', 'axes':'theta_dark:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(data_white={'value': self.white, 'units':'counts', 'axes':'theta_white:y:x', 'dataset_opts':  {'compression': 'gzip', 'compression_opts': 4} }))
            f.add_entry( DataExchangeEntry.data(title={'value': 'tomography_raw_projections'}))
            logger.info("Sample name = %s", sample_name)
            if (sample_name == None):
                sample_name = end[0]
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was assigned by the HDF5 converter and based on the HDF5 fine name'}))
                logger.info("Assigned default file name: %s", end[0])
            else:
                f.add_entry( DataExchangeEntry.sample( name={'value':sample_name}, description={'value':'Sample name was read from the user log file'}))
                logger.info("Assigned file name from user log")
                                
            f.close()
        else:
            if os.path.isfile(hdf5_file_name):
                print 'HDF5 already exists. Nothing to do ...'
            if (hdf5_file_extension == False):
                print "HDF file extension must be .h5 or .hdf"
