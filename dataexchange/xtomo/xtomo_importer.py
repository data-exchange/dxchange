# -*- coding: utf-8 -*-
"""Read tomographic image data from various format files.

Supported image fomats include TIFF, PackBits and LZW encoded TIFF, 
HDF5 (Data Exchange and NeXuS), HDF4 (NeXuS), SPE, TXRM, XRM, EDF, 
DPT, netCDF. 

.. module:: xtomo_importer.py
   :platform: Unix
   :synopsis: Import tomographic data files returning data, data_white, data_dark, theta.

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

Examples

>>> import dataexchange
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
>>> # Read raw data
>>> read = dataexchange.Import()
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

from dataexchange.xtomo.xtomo_reader import XTomoReader

class Import():
    def __init__(self, data=None, data_white=None,
                 data_dark=None, theta=None, color_log=True, stream_handler=True, log='INFO'):

        self.data = data
        self.data_white = data_white
        self.data_dark = data_dark
        self.theta = theta

        # Logging init.
        if color_log: # enable colored logging
            from dataexchange.tools import colorer

        # Set the log level.
        self.logger = None
        self._log_level = str(log).upper()
        self._init_logging(stream_handler)

    def xtomo_raw(self, file_name,
                         projections_start=0,
                         projections_end=0,
                         projections_step=1,
                         slices_start=0,
                         slices_end=0,
                         slices_step=1,
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
                         data_type='tiff',
                         exchange_rank = 0,
                         flip='false',
                         log='INFO'):
        """
        Read a stack of 2-D HDF4, TIFF, spe or netCDF images.

        Parameters
        
        file_name : str
            Base name of the input HDF4 or TIFF files.
            For example if the projections names are /local/data/test_XXXX.hdf
            file_name is /local/data/test_.hdf

        projections_start, projections_end, projections_step : scalar, optional
            start and end index for the projection
            images to load. Use step to define a stride.

        slices_start, slices_end, slices_step : scalar, optional
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
                - ``compressed_tiff``: tiff files used at elettra
                - ``dpt``: ASCII data from SRC infrared tomography
                - ``edf``: ESRF file format when projections, dark and white are in a single (large) edf files
                - ``edf2``: ESRF file format when projections, dark and white are each in a single file (series of files)s
                - ``nc``: netCDF data from 13-BM
                - ``nxs``: NeXuS Diamond Light Source
                - ``hdf4``: HDF4 files used on old detectors at APS 2-BM
                - ``h5``: Data Exchange HDF5
                - ``spe``: spe data from APS 13-BM
                - ``tiff``: uncompressed regualar tiff files used at Petra III, ALS, Elettra, SLS, Australia, CHESS
                - ``xradia``: txrm and xrm used by all Xradia systems


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


        # Determine file name and extension type.
        if (data_type is 'hdf4'):
            if file_name.endswith('h4') or \
                file_name.endswith('hdf'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('h4') or \
                white_file_name.endswith('hdf'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('h4') or \
                dark_file_name.endswith('hdf'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'hdf5'):
            if file_name.endswith('HDF') or \
                file_name.endswith('hdf'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('HDF') or \
                white_file_name.endswith('hdf'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('HDF') or \
                dark_file_name.endswith('hdf'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'nxs'):
            if file_name.endswith('NXS') or \
                file_name.endswith('nxs'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('NXS') or \
                white_file_name.endswith('nxs'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('NXS') or \
                dark_file_name.endswith('nxs'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'spe'):
            if file_name.endswith('SPE') or \
                file_name.endswith('spe'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('SPE') or \
                white_file_name.endswith('spe'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('SPE') or \
                dark_file_name.endswith('spe'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'nc'):
            if file_name.endswith('NC') or \
                file_name.endswith('nc'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('NC') or \
                white_file_name.endswith('nc'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('NC') or \
                dark_file_name.endswith('nc'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif ((data_type is 'tiff') or (data_type is 'compressed_tiff')):
            if file_name.endswith('tif') or \
                file_name.endswith('tiff'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]

            if white_file_name.endswith('tif') or \
                white_file_name.endswith('tiff'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('tif') or \
                dark_file_name.endswith('tiff'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'edf'):
            if file_name.endswith('EDF') or \
                file_name.endswith('edf'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('EDF') or \
                white_file_name.endswith('edf'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('EDF') or \
                dark_file_name.endswith('edf'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'edf2'):
            if file_name.endswith('EDF') or \
                file_name.endswith('edf'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('EDF') or \
                white_file_name.endswith('edf'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('EDF') or \
                dark_file_name.endswith('edf'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'dpt'):
            if file_name.endswith('DPT') or \
                file_name.endswith('dpt'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('DPT') or \
                white_file_name.endswith('dpt'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('DPT') or \
                dark_file_name.endswith('dpt'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'h5'):
            if exchange_rank > 0:
                exchange_base = 'exchange{:d}'.format(int(exchange_rank))
            else:
                exchange_base = "exchange"     

            if file_name.endswith('H5') or \
                file_name.endswith('h5'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('H5') or \
                white_file_name.endswith('h5'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('H5') or \
                dark_file_name.endswith('h5'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        elif (data_type is 'xradia'):
            if file_name.endswith('TXRM') or \
                file_name.endswith('txrm'):
                data_file = os.path.splitext(file_name)[0]
                dataExtension = os.path.splitext(file_name)[1]
            if white_file_name.endswith('XRM') or \
                white_file_name.endswith('xrm'):
                data_file_white = os.path.splitext(white_file_name)[0]
            if dark_file_name.endswith('XRM') or \
                dark_file_name.endswith('xrm'):
                data_file_dark = os.path.splitext(dark_file_name)[0]

        
        projections_file_index = ["" for x in range(projections_digits)]
        for m in range(projections_digits):
            if projections_zeros is True:
                projections_file_index[m] = '0' * (projections_digits-m-1)
            elif projections_zeros is False:
                projections_file_index[m] = ''

        white_file_index = ["" for x in range(white_digits)]
        for m in range(white_digits):
            if white_zeros is True:
                white_file_index[m] = '0' * (white_digits-m-1)
            elif white_zeros is False:
                white_file_index[m] = ''

        dark_file_index = ["" for x in range(dark_digits)]
        for m in range(dark_digits):
            if dark_zeros is True:
                dark_file_index[m] = '0' * (dark_digits-m-1)
            elif dark_zeros is False:
                dark_file_index[m] = ''

        self.logger.debug('')


        # Data ------------------------------------------------

        # Start reading projections one-by-one.
        ind = range(projections_start, projections_end, projections_step)
        _file_name = ' '
        for m in range(len(ind)):
            for n in range(projections_digits):
                if ind[m] < np.power(10, n+1):
                    _file_name = data_file + projections_file_index[n] + str(ind[m]) + dataExtension
                    self.logger.info("Generating projection file names: [%s]", _file_name)                    
                    break

            if os.path.isfile(_file_name):
                projection_exist = True
                self.logger.info("Reading projection file: [%s]", os.path.realpath(_file_name))
                self.logger.info("data type: [%s]", data_type)

                f = XTomoReader(_file_name)
                if (data_type is 'hdf4'):
                    tmpdata = f.hdf4(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')

                elif (data_type is 'hdf5'):
                    tmpdata = f.hdf5_2d(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='/entry/data/data')

                elif (data_type is 'compressed_tiff'):
                    tmpdata = f.tiffc(x_start=slices_start,
                                      x_end=slices_end,
                                      x_step=slices_step,
                                      dtype=dtype)

                elif (data_type is 'spe'):
                    tmpdata = f.spe(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)

                elif (data_type is 'nc'):
                    tmpdata = f.netcdf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
 
                elif (data_type is 'tiff'):
                    tmpdata = f.tiff(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     dtype=dtype,
                                     flip=flip)

                elif (data_type is 'edf2'):
                    tmpdata = f.edf2(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or
                    (data_type is 'edf2') or
                    (data_type is 'hdf5')):
                    if m == 0: # Get resolution once.
                        input_data = np.empty((len(ind), tmpdata.shape[0], tmpdata.shape[1]), dtype=dtype)
                    input_data[m, :, :] = tmpdata

                if ((data_type is 'spe') or
                    (data_type is 'nc')):
                    if m == 0: # Get resolution once.
                        input_data = np.vstack([tmpdata])
                    else:
                        input_data = np.concatenate((input_data, tmpdata), axis=0)

        # Update data.
        if projection_exist:
            self.data = input_data
            dtype = input_data.dtype

        else:
            self.logger.info("Attempt reading projections from: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_name = '/'.join([exchange_base, "data"])
                    tmpdata = f.hdf5(z_start = projections_start,
                                    	z_end = projections_end,
                                    	z_step = projections_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name= array_name)
                    self.data = tmpdata
            elif (data_type is 'nxs'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_type = 'projections'
                    tmpdata = f.nxs(z_start = projections_start,
                                    	z_end = projections_end,
                                    	z_step = projections_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_type= array_type)
                    self.data = tmpdata
            elif (data_type is 'edf'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data = tmpdata
            elif (data_type is 'xradia'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.txrm(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    dtype = tmpdata.dtype                    
                    self.data = tmpdata
            elif (data_type is 'dpt'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data = tmpdata
            else:
                self.logger.error("Projection file is mandatory")
            
        # White ------------------------------------------------

        # Reading white fields.
        ind = range(white_start, white_end, white_step)
        for m in range(len(ind)):
            for n in range(white_digits):
                if ind[m] < np.power(10, n+1):
                    _file_name = data_file_white + white_file_index[n] + str(ind[m]) + dataExtension
                    self.logger.info("Generating white file names: [%s]", _file_name)
                    break

            if os.path.isfile(_file_name):
                white_exist = True
                self.logger.info("Reading white file: [%s]", os.path.realpath(_file_name))
                self.logger.info("data type: [%s]", data_type)

                f = XTomoReader(_file_name)
                if (data_type is 'hdf4'):
                    tmpdata = f.hdf4(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')

                elif (data_type is 'hdf5'):
                    # to check on real data set from APS 15-ID
                    tmpdata = f.hdf5_2d(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')

                elif (data_type is 'compressed_tiff'):
                    tmpdata = f.tiffc(x_start=slices_start,
                                      x_end=slices_end,
                                      x_step=slices_step,
                                      dtype=dtype)

                elif (data_type is 'spe'):
                    tmpdata = f.spe(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)


                elif (data_type is 'nc'):
                    tmpdata = f.netcdf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)

                elif (data_type is 'tiff'):
                    tmpdata = f.tiff(x_start = slices_start,
                                     x_end = slices_end,
                                     x_step = slices_step,
                                     dtype=dtype,
                                     flip=flip)

                elif (data_type is 'edf2'):
                    tmpdata = f.edf2(x_start = slices_start,
                                     x_end = slices_end,
                                     x_step = slices_step)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or
                    (data_type is 'edf2') or
                    (data_type is 'hdf5')):
                    if m == 0: # Get resolution once.
                        input_data = np.empty((len(ind),
                                             tmpdata.shape[0],
                                             tmpdata.shape[1]),
                                             dtype=dtype)
                    input_data[m, :, :] = tmpdata

                if ((data_type is 'spe') or
                    (data_type is 'nc')):
                    if m == 0: # Get resolution once.
                        input_data = np.vstack([tmpdata])
                    else:
                        input_data = np.concatenate((input_data, tmpdata), axis=0)

        # Update white data.
        if white_exist:
            self.data_white = input_data
        else:
            self.logger.info("Attempt reading white from file: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the whites that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("White file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.hdf5(z_start = white_start,
                                    	z_end = white_end,
                                    	z_step = white_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
                                        x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                        array_name= '/'.join([exchange_base, "data_white"]))
                    self.data_white = tmpdata
                else:
                    # Fabricate one white field
                    self.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(self.data)
                    self.data_white = np.ones((1, ny, nx))
            elif (data_type is 'nxs'):
                # Read the whites that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("White file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_type = 'white'
                    tmpdata = f.nxs(z_start = white_start,
                                    	z_end = white_end,
                                    	z_step = white_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_type= array_type)
                    self.data_white = tmpdata
            elif (data_type is 'edf'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    self.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_white = tmpdata
                else:
                    # Fabricate one white field
                    self.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(self.data)
                    self.data_white = np.ones((1, ny, nx))
            elif (data_type is 'xradia'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    self.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.xrm(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_white = tmpdata
                else:
                    # Fabricate one white field
                    self.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(self.data)
                    self.data_white = np.ones((1, ny, nx),dtype=dtype)
            elif (data_type is 'dpt'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    self.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_white = tmpdata
                else:
                    # Fabricate one white field
                    self.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(self.data)
                    self.data_white = np.ones((1, ny, nx))
            else:
                # Fabricate one white field
                self.logger.warning("White file is missing. Generating white fields")
                nz, ny, nx = np.shape(self.data)
                self.data_white = np.ones((1, ny, nx), dtype=dtype)

        # Dark ------------------------------------------------

        # Reading dark fields.
        ind = range(dark_start, dark_end, dark_step)
        for m in range(len(ind)):
            for n in range(dark_digits):
                if ind[m] < np.power(10, n + 1):
                    _file_name = data_file_dark + dark_file_index[n] + str(ind[m]) + dataExtension
                    self.logger.info("Generating dark file names: [%s]", _file_name)
                    break

            if os.path.isfile(_file_name):
                dark_exist = True
                self.logger.info("Reading dark file: [%s]", os.path.realpath(_file_name))
                self.logger.info("data type: [%s]", data_type)

                f = XTomoReader(_file_name)
                if (data_type is 'hdf4'):
                    tmpdata = f.hdf4(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')

                elif (data_type is 'hdf5'):
                    # to check on real data set from APS 15-ID
                    tmpdata = f.hdf5_2d(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')

                elif (data_type is 'compressed_tiff'):
                    tmpdata = f.tiffc(x_start=slices_start,
                                      x_end=slices_end,
                                      x_step=slices_step,
                                      dtype=dtype)

                elif (data_type is 'spe'):
                    tmpdata = f.spe(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)

                elif (data_type is 'nc'):
                    tmpdata = f.netcdf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)

                elif (data_type is 'tiff'):
                    tmpdata = f.tiff(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     dtype=dtype,
                                     flip=flip)

                elif (data_type is 'edf2'):
                    tmpdata = f.edf2(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or 
                    (data_type is 'edf2') or
                    (data_type is 'hdf5')):
                    if m == 0: # Get resolution once.
                        input_data = np.empty((len(ind),
                                             tmpdata.shape[0],
                                             tmpdata.shape[1]),
                                             dtype=dtype)
                    input_data[m, :, :] = tmpdata

                if ((data_type is 'spe') or
                    (data_type is 'nc')):
                    if m == 0: # Get resolution once.
                        input_data = np.vstack([tmpdata])
                    else:
                        input_data = np.concatenate((input_data, tmpdata), axis=0)

        # Update dark data.
        if dark_exist > 0:
            self.data_dark = input_data
        else:
            self.logger.info("Attempt reading dark from file: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Dark file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.hdf5(z_start = dark_start,
                                    	z_end = dark_end,
                                    	z_step = dark_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
                                        x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name= '/'.join([exchange_base, "data_dark"]))
                    self.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    self.logger.warning("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(self.data)
                    self.data_dark = np.zeros((1, ny, nx))
            elif (data_type is 'nxs'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    self.logger.info("Dark file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    array_type = 'dark'
                    tmpdata = f.nxs(z_start = dark_start,
                                    	z_end = dark_end,
                                    	z_step = dark_step,
                                        y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_type= array_type)
                    self.data_dark = tmpdata
            elif (data_type is 'edf'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    self.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    self.logger.warning("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(self.data)
                    self.data_dark = np.zeros((1, ny, nx))
            elif (data_type is 'xradia'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    self.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.xrm(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    self.logger.warning("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(self.data)
                    self.data_dark = np.zeros((1, ny, nx),dtype=dtype)
            elif (data_type is 'dpt'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    self.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    self.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    self.logger.warning("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(self.data)
                    self.data_dark = np.zeros((1, ny, nx))
            else:
                # Fabricate one dark field
                self.logger.warning("Dark file is missing. Generating dark fields")
                nz, ny, nx = np.shape(self.data)
                self.data_dark = np.zeros((1, ny, nx), dtype=dtype)
        # Theta ------------------------------------------------
	if (data_type is 'h5'):
		self.logger.info("Attempt reading angles from file: [%s]", file_name)                    
		f = XTomoReader(file_name)
		self.logger.info("Angle file: [%s] exists", file_name) 
                array_name = '/'.join([exchange_base, "theta"])                   
		tmpdata = f.hdf5(z_start = projections_start, 
                        z_end = projections_end,
                        z_step = projections_step,
                        y_start = slices_start,
                        y_end = slices_end,
                        y_step = slices_step,
                        array_name=array_name)
		self.theta = tmpdata
	elif (data_type is 'xradia'):
		self.logger.info("Attempt reading angles from file: [%s]", file_name)                    
		f = XTomoReader(file_name)
        	self.logger.info("Angle file: [%s] exists", file_name)                    
		tmpdata = f.txrm(array_name='theta')
		self.theta = tmpdata
	else:
	        # Fabricate theta values
        	nz, ny, nx = np.shape(self.data)
        	z = np.arange(nz)
        	self.logger.warning("Angle file missing")                    
        	self.logger.warning("Generating angles")                    

        	projections_angle_range = projections_angle_end - projections_angle_start
        	self.theta = (z * float(projections_angle_range) / (len(z)))

        return self.data, self.data_white, self.data_dark, self.theta

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

