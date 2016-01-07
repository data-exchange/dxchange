# -*- coding: utf-8 -*-
"""Read tomographic image data from various format files.

Import tomographic raw data files as:

compressed_tiff  tiff files used at elettra
dpt              ASCII data from SRC infrared tomography
edf              ESRF file format when projections, dark and white are in a single (large) edf files
edf2             ESRF file format when projections, dark and white are each in a single file (series of files)s
nc               netCDF data from 13-BM
nxs              NeXus Diamond Light Source
h5               Data Exchange HDF5
spe              spe data from APS 13-BM
tiff             uncompressed regualar tiff files used at Petra III, ALS, Elettra, SLS, Australia, CHESS
xradia           txrm and xrm used by all Xradia systems

returning arrays for data, data_white, data_dark, theta ready for Data Exchange / tomoPy

.. module:: xtomo_importer.py
   :platform: Unix
   :synopsis: Import tomographic raw data files returning arrays for data, data_white, data_dark, theta.

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2015.07.9

Examples

>>> import xtomo_importer as xtomo_imp 
>>>  
>>> file_name = '/local/data/radios/image_.tif'
>>> dark_file_name = '/local/data/darks/image_.tif'
>>> white_file_name = '/local/data/flats/image_.tif'
>>> 
>>> hdf5_file_name = '/local/data/dataExchange/Anka.h5'
>>> 
>>> projections_start = 0
>>> projections_end = 3167
>>> white_start = 0
>>> white_end = 100
>>> dark_start = 0
>>> dark_end = 100
>>> 
>>> sample_name = 'Anka'
>>>     
>>> Read raw data
>>> read = xtomo_imp.Import()
>>> data, white, dark, theta = read.xtomo_raw(file_name,
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

"""

import h5py
import logging
import numpy as np
import os

from xtomo_reader import XTomoReader

class Import():
    def __init__(self, 
                    data=None, 
                    data_white=None,
                    data_dark=None, 
                    theta=None,
                    color_log=True, 
                    stream_handler=True, 
                    log='INFO'):

        self.data = data
        self.data_white = data_white
        self.data_dark = data_dark
        self.theta = theta

        # Logging init.
        if color_log: # enable colored logging
            import colorer

        # Set the log level.
        self.logger = None
        self._log_level = str(log).upper()
        self._init_logging(stream_handler)

    def xtomo_raw(self, file_name,
                         projections_start=0,
                         projections_end=0,
                         projections_step=1,
                         sino_start=0,
                         sino_end=0,
                         sino_step=1,
                         pixels_start=0,
                         pixels_end=0,
                         pixels_step=1,
                         white_file_name=None,
                         white_start=0,
                         white_end=0,
                         white_step=1,
                         dark_file_name=None,
                         dark_start=0,
                         dark_end=0,
                         dark_step=1,
                         projections_angle_start = 0,
                         projections_angle_end = 180,
                         projections_zeros=True,
                         projections_digits=-1,
                         white_digits=None,
                         dark_digits=None,
                         white_zeros=True,
                         dark_zeros=True,
                         dtype='uint16',
                         data_type='fabio',
                         exchange_rank = 0,
                         flip='false',
                         log='INFO'):
        """
        Read a stack of 2-D TIFF, spe or netCDF images.

        Parameters
        
        file_name : str
            Base name of the input TIFF files.
            For example if the projections names are /local/data/test_XXXX.hdf
            file_name is /local/data/test_.hdf

        projections_start, projections_end, projections_step : scalar, optional
            start and end index for the projection
            images to load. Use step to define a stride.

        sino_start, sino_end, sino_step : scalar, optional
            start and end pixel of the projection image to load
            along the rotation axis. Use step to define a stride.

        white_file_name, dark_file_name : str, optional
            Base name of the white and dark field input files.
            For example if the white field names
            are /local/data/test_bg_XXXX.hdf
            file_name is /local/data/test_bg_.hdf.
            If omitted white_file_name = file_name.

        white_start, white_end, white_step : scalar, optional
            start and end index for the white field
            files to load. Use step define a stride.

        dark_start, dark_end, dark_step : scalar, optional
            start and end index for the dark field
            files to load. Use step to define a stride.

        projections_digits, white_digits, dark_digits : scalar, optional
            Maximum number of digits used for file indexing.
            For example if last file is: test_9999.hdf _digits is 4
            if -1 skips series of file name generation and assume one sigle file is used for
            all projections, white or dark.

        projections_zeros, white_zeros, dark_zeros : bool, optional
            If ``True`` assumes all indexing uses projections_digits digits:
            if projections_digits = 4 and projections_zeros = true indeding is:
            (0001, 0002, ..., 9999).
            If ``False`` omits projections_zeros in
            indexing (1, 2, ..., 9999)

        sample_name : str, optional
            sample name. If not defined the file name is assigmed as sample name

        hdf5_file_name : str, optional
            if set the series for images is saved as a data exchange file

        dtype : str, optional
            Corresponding Numpy data type of file.

        data_type : str, optional
            supported options are:
compressed_tiff``: tiff files used at elettra
dpt``: ASCII data from SRC infrared tomography
edf``: ESRF file format when projections, dark and white are in a single (large) edf files
edf2``: ESRF file format when projections, dark and white are each in a single file (series of files)s
nc``: netCDF data from 13-BM
nxs``: NeXuS Diamond Light Source
h5``: Data Exchange HDF5
spe``: spe data from APS 13-BM
tiff``: uncompressed regualar tiff files used at Petra III, ALS, Elettra, SLS, Australia, CHESS
xradia``: txrm and xrm used by all Xradia systems


        exchange_rank : int, optional
            set when reading Data Exchange HDF5 files
            exchange rank is added to "exchange" to point tomopy to the data to recontruct.
            if rank is not set then the data are raw from the detector and are located under
            exchange = "exchange/...", to process data that are the result of some intemedite 
            processing step then exchange_rank = 1 will direct tomopy to process "exchange1/..."

        Returns
        
        Output : data, data_white, data_dark, theta

       """
        projection_exist = False
        dark_exist = False
        white_exist = False

        if (projections_digits == -1):
            # Set default dark/white file names
            if white_file_name is None:
                    white_file_name = "does_not_exist"
            if dark_file_name is None:
                    dark_file_name = "does_not_exist"
            
        else:    
            # Set default prefix for white and dark series of files.
            if white_file_name is None:
                    white_file_name = file_name
            if dark_file_name is None:
                    dark_file_name = file_name

        # Set default digits.
        if white_digits is None:
            white_digits = projections_digits
        if dark_digits is None:
            dark_digits = projections_digits


        self.logger.debug('')


        # Start reading images
        self.data = self.xtomo_read_images(file_name,
                         images_start=projections_start,
                         images_end=projections_end,
                         images_step=projections_step,
                         sino_start=sino_start,
                         sino_end=sino_end,
                         sino_step=sino_step,
                         pixels_start=pixels_start,
                         pixels_end=pixels_end,
                         pixels_step=pixels_step,
                         images_digits=projections_digits,
                         images_zeros=projections_zeros,
                         dtype=dtype,
                         data_type=data_type,
                         #array_type = array_type, 
                         flip=flip)

        self.data_white = self.xtomo_read_images(white_file_name,
                         images_start=white_start,
                         images_end=white_end,
                         images_step=white_step,
                         sino_start=sino_start,
                         sino_end=sino_end,
                         sino_step=sino_step,
                         pixels_start=pixels_start,
                         pixels_end=pixels_end,
                         pixels_step=pixels_step,
                         images_digits=white_digits,
                         images_zeros=white_zeros,
                         dtype=dtype,
                         data_type=data_type,
                         #array_type = array_type, 
                         flip=flip)

        self.data_dark = self.xtomo_read_images(dark_file_name,
                         images_start=dark_start,
                         images_end=dark_end,
                         images_step=dark_step,
                         sino_start=sino_start,
                         sino_end=sino_end,
                         sino_step=sino_step,
                         pixels_start=pixels_start,
                         pixels_end=pixels_end,
                         pixels_step=pixels_step,
                         images_digits=dark_digits,
                         images_zeros=dark_zeros,
                         dtype=dtype,
                         data_type=data_type,
                         #array_type = array_type, 
                         flip=flip)

        self.theta = self.xtomo_generate_theta(images_angle_start = projections_angle_start,
                         images_angle_end = projections_angle_end)

        if (self.data == None):
                self.logger.error("Projection file is mandatory")                   
        if (self.data_white == None):
                self.data_white = self.xtomo_generate_white(tomo = self.data, dtype = dtype)              
        if (self.data_dark == None):
                self.data_dark = self.xtomo_generate_dark(tomo = self.data, dtype = dtype)              
      
        return self.data, self.data_white, self.data_dark, self.theta

    def xtomo_read_images(self, file_name,
                         images_start=0,
                         images_end=0,
                         images_step=1,
                         sino_start=0,
                         sino_end=0,
                         sino_step=1,
                         pixels_start=0,
                         pixels_end=0,
                         pixels_step=1,
                         images_digits=-1,
                         images_zeros=True,
                         dtype='uint16',
                         data_type='fabio',
                         array_type='projections',
                         flip='false',
                         log='INFO'):

        # Determine file name and extension type.
        data_file = os.path.splitext(file_name)[0]
        data_extension = os.path.splitext(file_name)[1]

        images_file_index = ["" for x in range(images_digits)]
        for m in range(images_digits):
            if images_zeros is True:
                images_file_index[m] = '0' * (images_digits-m-1)
            elif images_zeros is False:
                images_file_index[m] = ''

        _file_name = ' '
        image_exist = False
        # Start reading projections one-by-one.
        ind = range(images_start, images_end, images_step)
        for m in range(len(ind)):
            for n in range(images_digits):
                if ind[m] < np.power(10, n+1):
                    _file_name = data_file + images_file_index[n] + str(ind[m]) + data_extension
                    self.logger.info("Generating image file names: [%s]", _file_name)                    
                    break

            if os.path.isfile(_file_name):
                image_exist = True
                self.logger.info("Reading image file: [%s]", os.path.realpath(_file_name))
                self.logger.info("data type: [%s]", data_type)

                f = XTomoReader(_file_name)

                if (data_type is 'spe'):
                    tmpdata = f.spe(y_start = sino_start,
                                    y_end = sino_end,
                                    y_step = sino_step)

                elif (data_type is 'nc'):
                    tmpdata = f.netcdf(y_start = sino_start,
                                    y_end = sino_end,
                                    y_step = sino_step)

                elif (data_type is 'tiff'):
                    tmpdata = f.tiff(x_start=sino_start,
                                     x_end=sino_end,
                                     x_step=sino_step,
                                     dtype=dtype,
                                     flip=flip)

                elif (data_type is 'compressed_tiff'):
                    tmpdata = f.tiffc(x_start=sino_start,
                                      x_end=sino_end,
                                      x_step=sino_step,
                                      dtype=dtype)
 
                elif (data_type is 'hdf5'):
                    tmpdata = f.hdf5_2d(x_start=sino_start,
                                     x_end=sino_end,
                                     x_step=sino_step,
                                     array_name ='/entry1/data/data')

                elif (data_type is 'edf2'):
                    tmpdata = f.edf2(x_start=sino_start,
                                     x_end=sino_end,
                                     x_step=sino_step)

                elif (data_type is 'fabio'):
                    tmpdata = f.fabio(x_start=sino_start,
                                     x_end=sino_end,
                                     x_step=sino_step,
                                     flip=flip)

                if ((data_type is 'spe') or
                    (data_type is 'nc')):
                    if m == 0: # Get resolution once.
                        input_data = np.vstack([tmpdata])
                    else:
                        input_data = np.concatenate((input_data, tmpdata), axis=0)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf5') or
                    (data_type is 'edf2') or
                    (data_type is 'fabio')):
                    if m == 0: # Get resolution once.
                        input_data = np.empty((len(ind), tmpdata.shape[0], tmpdata.shape[1]), dtype=dtype)
                    input_data[m, :, :] = tmpdata

        # Update data.
        if image_exist:
            data = input_data
            dtype = input_data.dtype

        elif (file_name == "does_not_exist"):        
            self.logger.error("image file [%s]", file_name)
            data = None

        else:
            self.logger.info("Attempt reading images from a single file: [%s]", file_name)
            data = None                    
            if (data_type is 'h5'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Image file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_name = '/'.join([exchange_base, "data"])
                    tmpdata = f.hdf5(z_start = images_start,
                                    	z_end = images_end,
                                    	z_step = images_step,
                                        y_start = sino_start,
                                    	y_end = sino_end,
                                    	y_step = sino_step,
                                        x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name = array_name)
                    data = tmpdata
            elif (data_type is 'nxs'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Image file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_type = 'projections'
                    tmpdata = f.nxs(z_start = images_start,
                                    	z_end = images_end,
                                    	z_step = images_step,
                                        y_start = sino_start,
                                    	y_end = sino_end,
                                    	y_step = sino_step,
                                        x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_type = array_type)
                    data = tmpdata
            elif (data_type is 'edf'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Image file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.edf(y_start = sino_start,
                                    y_end = sino_end,
                                    y_step = sino_step)
                    data = tmpdata
            elif (data_type is 'xradia'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Image file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.txrm(y_start = sino_start,
                                    y_end = sino_end,
                                    y_step = sino_step)
                    data = tmpdata
                    dtype = tmpdata.dtype                    
            elif (data_type is 'dpt'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Image file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.dpt(y_start = sino_start,
                                    y_end = sino_end,
                                    y_step = sino_step)
                    data = tmpdata
            else:
                data = None
                self.logger.error("No valid images found")
                self.logger.error("Missng white/dark images will be generated")

        return data


    def xtomo_generate_dark(self, tomo, dtype):

        self.logger.warning("Dark file is missing. Generating dark fields")
        nz, ny, nx = np.shape(tomo)
        dark = np.zeros((1, ny, nx), dtype=dtype)

        return dark

    def xtomo_generate_white(self, tomo, dtype):

        self.logger.warning("White file is missing. Generating white fields")
        nz, ny, nx = np.shape(tomo)
        white = np.ones((1, ny, nx), dtype=dtype)

        return white

    def xtomo_generate_theta(self,
                         images_angle_start,
                         images_angle_end,
                         log='INFO'):

        nz, ny, nx = np.shape(self.data)
        z = np.arange(nz)
        self.logger.warning("Generating angles [degrees]: start [%d]; end [%d]", images_angle_start, images_angle_end)                    

        images_angle_range = images_angle_end - images_angle_start
        theta = (z * float(images_angle_range) / (len(z)))

        return theta

    def _init_logging(self, stream_handler):
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

