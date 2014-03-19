# -*- coding: utf-8 -*-
import h5py
from pyhdf import SD
import numpy as np 
import PIL.Image as Image
import netCDF4 as nc

from formats.elettra.tifffile import TiffFile
import formats.xradia.xradia_xrm as xradia
import formats.xradia.data_struct as dstruct
import formats.aps_13bm.data_spe as spe
from formats.esrf.EdfFile import EdfFile

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
        Read 3-D tomographic data from hdf5 file.

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
        Read 2-D tomographic data from hdf4 file.

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
        dataset = hdfdata[y_start:y_end:y_step,
                          x_start:x_end:x_step]
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
        Read TIFF files.

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
        Read complex(!) TIFF files.

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
        Read 3-D tomographic data from a txrm file 
        
        Parameters
        ----------
        file_name : str
            Input txrm or xrm file.
        
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
        Read 3-D tomographic data from a xrm file.
        
        Parameters
        ----------
        file_name : str
            Input txrm or xrm file.
        
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
        Read 3-D tomographic data from a spe file.
        
        Parameters
        ----------
        file_name : str
            Input txrm or xrm file.

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
        
        
    def esrf(self,
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
        Read 3-D tomographic data from a 
        xradia (txrm) and ESRF (edf) file.
        
        Parameters
        ----------
        file_name : str
            Input txrm or xrm file.
            
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
        Read 3-D tomographic data from a netcdf file.

       
        Parameters
        ----------
        file_name : str
            Input txrm or xrm file.
        
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
