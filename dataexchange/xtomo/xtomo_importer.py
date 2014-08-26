# -*- coding: utf-8 -*-
"""Read image data from various format files.

.. module:: xtomo_importer.py
   :platform: Unix
   :synopsis: Import tomographic data files returnin: data, data_white, data_dark, theta.

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15


Examples
--------

>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 
>>> add example here 

"""

import numpy as np
import os
import h5py
import logging

from dataexchange.xtomo.xtomo_reader import XTomoReader

class Import():
    def __init__(xtomo, data=None, data_white=None,
                 data_dark=None, theta=None, log='INFO'):

        xtomo.data = data
        xtomo.data_white = data_white
        xtomo.data_dark = data_dark
        xtomo.theta = theta

        # Set the log level.
        xtomo.logger = None
        xtomo._log_level = str(log).upper()
        xtomo._init_logging()

    def series_of_images(xtomo, file_name,
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
#                         sample_name=None,
                         log='INFO'):
        """
        Read a stack of 2-D HDF4, TIFF, spe or netCDF images.

        Parameters
        ----------
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
                - ``hdf4``: HDF4 files used on old detectors at APS 2-BM
                - ``compressed_tiff``: tiff files used at elettra
                - ``tiff``: uncompressed regualar tiff files used at Petra III, ALS, Elettra, SLS, Australia, CHESS
                - ``spe``: spe data from APS 13-BM
                - ``nc``: netCDF data from 13-BM
                - ``dpt``: ASCII data from SRC infrared tomography

        Returns
        -------
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

        xtomo.logger.debug('')


        # Data ------------------------------------------------

        # Start reading projections one-by-one.
        ind = range(projections_start, projections_end, projections_step)
        for m in range(len(ind)):
            for n in range(projections_digits):
                if ind[m] < np.power(10, n+1):
                    _file_name = data_file + projections_file_index[n] + str(ind[m]) + dataExtension
                    xtomo.logger.info("Generating projection file names: [%s]", _file_name)                    
                    break

            if os.path.isfile(_file_name):
                projection_exist = True
                xtomo.logger.info("Reading projection file: [%s]", os.path.realpath(_file_name))
                xtomo.logger.info("data type: [%s]", data_type)

                f = XTomoReader(_file_name)
                if (data_type is 'hdf4'):
                    tmpdata = f.hdf4(x_start=slices_start,
                                     x_end=slices_end,
                                     x_step=slices_step,
                                     array_name='data')
		    print tmpdata.shape

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
                                     dtype='uint16')

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or
                    (data_type is 'hdf5')):
                    if m == 0: # Get resolution once.
			print len(ind), tmpdata.shape[0], tmpdata.shape[1], dtype
                        input_data = np.empty((len(ind), tmpdata.shape[0], tmpdata.shape[1]), dtype=dtype)
			print input_data.shape
                    input_data[m, :, :] = tmpdata

                if ((data_type is 'spe') or
                    (data_type is 'nc')):
                    if m == 0: # Get resolution once.
                        input_data = np.vstack([tmpdata])
                    else:
                        input_data = np.concatenate((input_data, tmpdata), axis=0)

        # Update data.
        if projection_exist:
            xtomo.data = input_data

        else:
	    # set new defaults
	     
            xtomo.logger.info("Attempt reading projection from file: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.hdf5(z_start = projections_start,
                                    	z_end = projections_end,
                                    	z_step = projections_step,
					                    y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					                    x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name='exchange/data')
                    xtomo.data = tmpdata
            elif (data_type is 'edf'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data = tmpdata
            elif (data_type is 'xradia'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.txrm()
                    xtomo.data = tmpdata
            elif (data_type is 'dpt'):
                # Read the projections that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("Projection file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data = tmpdata
            else:
                xtomo.logger.error("ERROR: Projection file is mandatory")
            
        # White ------------------------------------------------

        # Reading white fields.
        ind = range(white_start, white_end, white_step)
        for m in range(len(ind)):
            for n in range(white_digits):
                if ind[m] < np.power(10, n+1):
                    _file_name = data_file_white + white_file_index[n] + str(ind[m]) + dataExtension
                    xtomo.logger.info("Generating white file names: [%s]", _file_name)
                    break

            if os.path.isfile(_file_name):
                white_exist = True
                xtomo.logger.info("Reading white file: [%s]", os.path.realpath(_file_name))
                xtomo.logger.info("data type: [%s]", data_type)

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
                                     dtype = dtype)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or
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
            xtomo.data_white = input_data
        else:
            xtomo.logger.info("Attempt reading white from file: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the whites that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("White file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.hdf5(z_start = projections_start,
                                    	z_end = projections_end,
                                    	z_step = projections_step,
					y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name='exchange/data_white')
                    xtomo.data_white = tmpdata
                else:
                    # Fabricate one white field
                    xtomo.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_white = np.ones((1, ny, nx))
            elif (data_type is 'edf'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    xtomo.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data_white = tmpdata
                else:
                    # Fabricate one white field
                    xtomo.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_white = np.ones((1, ny, nx))
            elif (data_type is 'xradia'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    xtomo.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.xrm()
                    xtomo.data_white = tmpdata
                else:
                    # Fabricate one white field
                    xtomo.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_white = np.ones((1, ny, nx))
            elif (data_type is 'dpt'):
                # Read the whites that are all in a single file
                if os.path.isfile(white_file_name):
                    xtomo.logger.info("White file: [%s] exists", white_file_name)                    
                    f = XTomoReader(white_file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data_white = tmpdata
                else:
                    # Fabricate one white field
                    xtomo.logger.info("White file [%s]. Generating white fields", white_file_name)  
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_white = np.ones((1, ny, nx))
            else:
                # Fabricate one white field
                xtomo.logger.info("White file is missing. Generating white fields")
                nz, ny, nx = np.shape(xtomo.data)
                xtomo.data_white = np.ones((1, ny, nx))

        # Dark ------------------------------------------------

        # Reading dark fields.
        ind = range(dark_start, dark_end, dark_step)
        for m in range(len(ind)):
            for n in range(dark_digits):
                if ind[m] < np.power(10, n + 1):
                    _file_name = data_file_dark + dark_file_index[n] + str(ind[m]) + dataExtension
                    xtomo.logger.info("Generating dark file names: [%s]", _file_name)
                    break

            if os.path.isfile(_file_name):
                dark_exist = True
                xtomo.logger.info("Reading dark file: [%s]", os.path.realpath(_file_name))
                xtomo.logger.info("data type: [%s]", data_type)

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
                                     dtype=dtype)

                if ((data_type is 'tiff') or
                    (data_type is 'compressed_tiff') or
                    (data_type is 'hdf4') or 
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
            xtomo.data_dark = input_data
        else:
            xtomo.logger.info("Attempt reading dark from file: [%s]", file_name)                    
            if (data_type is 'h5'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(file_name):
                    xtomo.logger.info("Dark file: [%s] exists", file_name)                    
                    f = XTomoReader(file_name)
                    tmpdata = f.hdf5(z_start = projections_start,
                                    	z_end = projections_end,
                                    	z_step = projections_step,
					y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					x_start = pixels_start,
                                    	x_end = pixels_end,
                                    	x_step = pixels_step,
                                    	array_name='exchange/data_dark')
                    xtomo.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    xtomo.logger.info("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_dark = np.zeros((1, ny, nx))
            elif (data_type is 'edf'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    xtomo.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.edf(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    xtomo.logger.info("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_dark = np.zeros((1, ny, nx))
            elif (data_type is 'xradia'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    xtomo.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.xrm()
                    xtomo.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    xtomo.logger.info("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_dark = np.zeros((1, ny, nx))
            elif (data_type is 'dpt'):
                # Read the dark fields that are all in a single file
                if os.path.isfile(dark_file_name):
                    xtomo.logger.info("Dark file: [%s] exists", dark_file_name)                    
                    f = XTomoReader(dark_file_name)
                    tmpdata = f.dpt(y_start = slices_start,
                                    y_end = slices_end,
                                    y_step = slices_step)
                    xtomo.data_dark = tmpdata
                else:
                    # Fabricate one dark field
                    xtomo.logger.info("Dark file [%s]. Generating dark fields", dark_file_name)
                    nz, ny, nx = np.shape(xtomo.data)
                    xtomo.data_dark = np.zeros((1, ny, nx))
            else:
                # Fabricate one dark field
                xtomo.logger.info("Dark file is missing. Generating dark fields")
                nz, ny, nx = np.shape(xtomo.data)
                xtomo.data_dark = np.zeros((1, ny, nx))
        # Theta ------------------------------------------------
	if (data_type is 'h5'):
		xtomo.logger.info("Attempt reading angles from file: [%s]", file_name)                    
		f = XTomoReader(file_name)
		xtomo.logger.info("Angle file: [%s] exists", file_name)                    
		tmpdata = f.hdf5(z_start = projections_start,
					z_end = projections_end,
                                    	z_step = projections_step,
					y_start = slices_start,
                                    	y_end = slices_end,
                                    	y_step = slices_step,
					array_name='exchange/theta')
		xtomo.theta = tmpdata
	else:
	        # Fabricate theta values
        	nz, ny, nx = np.shape(xtomo.data)
        	z = np.arange(nz)

        	projections_angle_range = projections_angle_end - projections_angle_start
        	xtomo.theta = (z * float(projections_angle_range) / (len(z)))

        return xtomo.data, xtomo.data_white, xtomo.data_dark, xtomo.theta

    def _init_logging(xtomo):
        """
        Setup and start command line logging.
        """
        # Top-level log setup.
        xtomo.logger = logging.getLogger("data exchange")
        if xtomo._log_level == 'DEBUG':
            xtomo.logger.setLevel(logging.DEBUG)
        elif xtomo._log_level == 'INFO':
            xtomo.logger.setLevel(logging.INFO)
        elif xtomo._log_level == 'WARN':
            xtomo.logger.setLevel(logging.WARN)
        elif xtomo._log_level == 'WARNING':
            xtomo.logger.setLevel(logging.WARNING)
        elif xtomo._log_level == 'ERROR':
            xtomo.logger.setLevel(logging.ERROR)

        # Terminal stream log.
        ch = logging.StreamHandler()
        if xtomo._log_level == 'DEBUG':
            ch.setLevel(logging.DEBUG)
        elif xtomo._log_level == 'INFO':
            ch.setLevel(logging.INFO)
        elif xtomo._log_level == 'WARN':
            ch.setLevel(logging.WARN)
        elif xtomo._log_level == 'WARNING':
            ch.setLevel(logging.WARNING)
        elif xtomo._log_level == 'ERROR':
            ch.setLevel(logging.ERROR)

        # Show date and time.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Update logger.
        if not len(xtomo.logger.handlers): # For fist time create handlers.
            xtomo.logger.addHandler(ch)

# Nexus not working yet
    def nexus(xtomo, file_name,
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
        """
        Read Data Exchange HDF5 file.

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

        f = XTomoReader()
        # Read data from exchange group.
        xtomo.data = f.hdf5(file_name,
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
        xtomo.data_white = f.hdf5(file_name,
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
        xtomo.data_dark = f.hdf5(file_name,
                            array_name=array_name,
                            x_start=dark_start,
                            x_end=dark_end,
                            y_start=slices_start,
                            y_end=slices_end,
                            y_step=slices_step,
                            z_start=pixels_start,
                            z_end=pixels_end,
                            z_step=pixels_step).astype(dtype)

