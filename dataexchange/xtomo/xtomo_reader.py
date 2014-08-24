# -*- coding: utf-8 -*-
"""Read image data from various format files.

This module provides file format support to xtomo_importer 

Supported image fomats include TIFF, PackBits and LZW encoded TIFF, 
HDF5 (Data Exchange and NeXuS), HDF4 (NeXuS), SPE, TXRM, XRM, EDF, 
DPT, netCDF. 

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

Requirements
------------
* `h5py <http://www.h5py.org/>`_ 
* `PIL.Image <http://www.pythonware.com/products/pil/>`_ 
* `pyhdf <https://pypi.python.org/pypi/pyhdf>`_  (optional for supporting APS 2-BM data)
* `netCDF <https://pypi.python.org/pypi/netCDF4>`_  (optional for supporting APS 13-BM data)
* `Tifffile.c 2013.01.18 <http://www.lfd.uci.edu/~gohlke/>`_ (optional for supporting Elettra data)
  (recommended for faster decoding of PackBits and LZW encoded strings)

Notes
-----
Tested on little-endian platforms only.

Examples
--------

>>> f = XTomoReader(_file_name)
>>> if (data_type is 'hdf4'):
>>>     tmpdata = f.hdf4(x_start=slices_start,
>>>                         x_end=slices_end,
>>>                         x_step=slices_step,
>>>                         array_name='data')

"""

import h5py
from pyhdf import SD
import numpy as np 
import PIL.Image as Image
import netCDF4 as nc
import math
import os

import formats.xradia_xrm as xradia
import formats.data_struct as dstruct
import formats.data_spe as spe

from formats.EdfFile import EdfFile
from formats.tifffile import TiffFile

class XTomoReader:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def hdf5(self,
             array_name=None,
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1,
             z_start=0,
             z_end=None,
             z_step=1):
        """ 
        Read 3-D tomographic projection data from a Data Exchange HDF5 file.

        Opens ``file_name`` and reads the contents of the 3D array specified 
	by ``array_name`` in the specified group of the HDF5 file.
        
        Parameters
        ----------
        file_name : str
            Input HDF5 file.
        
        array_name : str
            Name of the array to be read at in the exchange group.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        Returns
        -------
        out : ndarray
            Returns the data as a matrix.
        """
        # Read data from file.
        f = h5py.File(self.file_name, 'r')
        hdfdata = f[array_name]
        num_x, num_y, num_z = hdfdata.shape

        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset.
        dataset = hdfdata[x_start:x_end:x_step,
                          y_start:y_end:y_step,
                          z_start:z_end:z_step]
	print dataset.shape
        f.close()
        return dataset
                
    def hdf4(self,
             array_name=None,
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1):
        """ 
        Read 2-D tomographic projection data from an HDF4 file.

        Opens ``file_name`` and reads the contents
        of the array specified by ``array_name`` in
        the specified group of the HDF file.
        
        Parameters
        ----------
        file_name : str
            Input HDF file.
        
        array_name : str
            Name of the array to be read at exchange group.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        Returns
        -------
        out : ndarray
            Returns the data as a matrix.
        """
        # Read data from file.
        f = SD.SD(self.file_name)
        sds = f.select(array_name)
        hdfdata = sds.get()
        sds.endaccess()
        f.end()

        num_y, num_x = hdfdata.shape
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y

        # Construct dataset.
        dataset = hdfdata[x_start:x_end:x_step,
                          y_start:y_end:y_step]
        return dataset
        
    def hdf5_2d(self,
             array_name=None,
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1):
        """ 
        Read 2-D tomographic projection data from an HDF5 file.

        Opens ``file_name`` and reads the contents
        of the array specified by ``array_name`` in
        the specified group of the HDF file.
        
        Parameters
        ----------
        file_name : str
            Input HDF file.
        
        array_name : str
            Name of the array to be read at exchange group.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        Returns
        -------
        out : ndarray
            Returns the data as a matrix.
        """
        # Read data from file.
        f = h5py.File(self.file_name, 'r')
        hdfdata = f[array_name]

        #print array_name

        num_x, num_y = hdfdata.shape
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y

        # Construct dataset.
        dataset = hdfdata[x_start:x_end:x_step,
                          y_start:y_end:y_step]
        f.close()
        return dataset
        
    def tiff(self, 
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1,
             dtype='uint16'
             ):
             
        """
        Read 2-D tomographic projection data from a TIFF file.

        Parameters
        ----------
        file_name : str
            Name of the input TIFF file.
        
        dtype : str, optional
            Corresponding numpy data type of the TIFF file.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        Returns
        -------
        out : ndarray
            Output 2-D matrix as numpy array.
        """
        im = Image.open(self.file_name)
        out = np.fromstring(im.tostring(), dtype).reshape(
                               tuple(list(im.size[::-1])))

        num_x, num_y = out.shape

        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        
        #im.close()
        return out[x_start:x_end:x_step,
                   y_start:y_end:y_step]
        
    def tiffc(self, 
              dtype='uint16',
              x_start=0,
              x_end=None,
              x_step=1,
              y_start=0,
              y_end=None,
              y_step=1):
        """
        Read 2-D complex(!) tomographic projection data from a TIFF file.

        Parameters
        ----------
        file_name : str
            Name of the input TIFF file.
        
        dtype : str, optional
            Corresponding Numpy data type of the TIFF file.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole ndarray.
        
        Returns
        -------
        out : ndarray
            Output 2-D matrix as numpy array.
        """
        im = TiffFile(self.file_name)
        out = im[0].asarray()

        num_x, num_y = out.shape
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        
        #im.close()
        return out[x_start:x_end:x_step,
                   y_start:y_end:y_step]
        
    def txrm(self,
             array_name='Image',
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1,
             z_start=0,
             z_end=None,
             z_step=1):
        """ 
        Read 3-D tomographic projection data from a TXRM file 
        
        Parameters
        ----------
        file_name : str
            Input txrm file.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
        reader = xradia.xrm()
        array = dstruct

        # Read data from file.
        reader.read_txrm(self.file_name, array)
        num_x, num_y, num_z = np.shape(array.exchange.data)
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset.
        dataset = array.exchange.data[x_start:x_end:x_step,
                                      y_start:y_end:y_step,
                                      z_start:z_end:z_step]
        return dataset
       
    def xrm(self,
            array_name='Image',
            x_start=0,
            x_end=None,
            x_step=1,
            y_start=0,
            y_end=None,
            y_step=1,
            z_start=0,
            z_end=None,
            z_step=1):
        """ 
        Read 3-D tomographic projection data from an XRM file.
        
        Parameters
        ----------
        file_name : str
            Input xrm file.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
        reader = xradia.xrm()
        array = dstruct

        # Read data from file.
        reader.read_xrm(self.file_name,array)
        num_x, num_y, num_z = np.shape(array.exchange.data)
            
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset from desired y.
        dataset = array.exchange.data[x_start:x_end:x_step,
                                      y_start:y_end:y_step,
                                      z_start:z_end:z_step]
        return dataset
        
    def spe(self,
            x_start=0,
            x_end=None,
            x_step=1,
            y_start=0,
            y_end=None,
            y_step=1,
            z_start=0,
            z_end=None,
            z_step=1):
        """ 
        Read 3-D tomographic projection data from a SPE file.
        
        Parameters
        ----------
        file_name : str
            Input spe file.

        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
        spe_data = spe.PrincetonSPEFile(self.file_name)
        array = spe_data.getData()
        num_z, num_y, num_x = np.shape(array)

        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset from desired y.
        dataset = array[z_start:z_end:z_step,
                        y_start:y_end:y_step,
                        x_start:x_end:x_step]
        return dataset
        
    def edf(self,
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1,
             z_start=0,
             z_end=None,
             z_step=1):
        """ 
        Read 3-D tomographic projection data from an EDF (ESRF) file.
        
        Parameters
        ----------
        file_name : str
            Input edf file.
            
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
 
        # Read data from file.
        f = EdfFile(self.file_name, access='r')
        dic = f.GetStaticHeader(0)
        tmpdata = np.empty((f.NumImages, int(dic['Dim_2']), int(dic['Dim_1'])))

        for (i, ar) in enumerate(tmpdata):
            tmpdata[i::] = f.GetData(i)

        num_z, num_y, num_x = np.shape(tmpdata)
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset from desired y.
        dataset = tmpdata[z_start:z_end:z_step,
                          y_start:y_end:y_step,
                          x_start:x_end:x_step]
        #print np.shape(dataset)
        return dataset
        
    def dpt(self,
             x_start=0,
             x_end=None,
             x_step=1,
             y_start=0,
             y_end=None,
             y_step=1,
             z_start=0,
             z_end=None,
             z_step=1):
        """ 
        Read 3-D tomographic projection data from a DPT (SRC) file.
        
        Parameters
        ----------
        file_name : str
            Input dpt file.
            
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
 
        # Read data from file.
        offset = 2

        # Count the number of projections
        file = open(self.file_name, 'r')
        num_of_projections = sum(1 for line in file)
        file.close()

        # Determine image size and dimentions        
        file = open(self.file_name, 'r')
        first_line = file.readline()
        firstlinelist=first_line.split(",")

        image_size = len(firstlinelist)-offset
        image_dim = int(math.sqrt(image_size))
        file.close()

        tmpdata = np.empty((num_of_projections, image_dim, image_dim))
 
        num_z, num_y, num_x = np.shape(tmpdata)

        if image_dim**2 == image_size: # check projections are square
            print "Reading ", os.path.basename(self.file_name)
            file = open(self.file_name, 'r')      
            for line in file:
                linelist=line.split(",")

                projection = np.reshape(np.array(linelist)[offset:], (image_dim ,image_dim))

                projection = projection.transpose()
                projection = projection.astype(np.float)
                projection = np.exp(-projection)

                tmpdata[int(linelist[0])::] = projection

            file.close()

        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset from desired y.
        dataset = tmpdata[z_start:z_end:z_step,
                          y_start:y_end:y_step,
                          x_start:x_end:x_step]

        return dataset
       
    def netcdf(self,
               x_start=0,
               x_end=None,
               x_step=1,
               y_start=0,
               y_end=None,
               y_step=1,
               z_start=0,
               z_end=None,
               z_step=1):
        """ 
        Read 3-D tomographic projection data from a netCDF file.

       
        Parameters
        ----------
        file_name : str
            Input netcdf file.
        
        x_start, x_end, x_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        y_start, y_end, y_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        z_start, z_end, z_step : scalar, optional
            Values of the start, end and step of the
            slicing for the whole array.
        
        Returns
        -------
        out : array
            Returns the data as a matrix.
        """
        nc_data = nc.Dataset(self.file_name, 'r')
        array = nc_data.variables['array_data'][:]
            
        num_z, num_y, num_x = np.shape(array)
        if x_end is None:
            x_end = num_x
        if y_end is None:
            y_end = num_y
        if z_end is None:
            z_end = num_z

        # Construct dataset from desired y.
        dataset = array[z_start:z_end:z_step,
                        y_start:y_end:y_step,
                        x_start:x_end:x_step]
        return dataset
