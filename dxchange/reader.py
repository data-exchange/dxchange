#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2015, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2015. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

"""
Module for importing data files.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import six
import os
import h5py
import logging
import re
import math
import struct
from contextlib import contextmanager
import dxchange.writer as writer
from dxchange.dtype import empty_shared_array
import warnings
import functools
import tifffile
import scipy.misc as sm
import pandas as pd
from itertools import cycle
from io import StringIO

__author__ = "Doga Gursoy, Francesco De Carlo"
__copyright__ = "Copyright (c) 2015-2016, UChicago Argonne, LLC."
__version__ = "0.1.0"
__docformat__ = 'restructuredtext en'
__all__ = ['read_edf',
           'read_hdf5',
           'read_netcdf4',
           'read_npy',
           'read_spe',
           'read_fits',
           'read_tiff',
           'read_tiff_stack',
           'read_xrm',
           'read_xrm_stack',
           'read_aps_1id_metafile',
           'read_txrm',
           'read_hdf5_stack',
           'read_file_list']

logger = logging.getLogger(__name__)


def _check_import(modname):
    try:
        return __import__(modname)
    except ImportError:
        logger.warn(modname + ' module not found')
        return None

# Optional dependencies.
spefile = _check_import('spefile')
netCDF4 = _check_import('netCDF4')
EdfFile = _check_import('EdfFile')
astropy = _check_import('astropy')
olefile = _check_import('olefile')

# FIXME: raise exception would make more sense, also not sure an extension check
# is very useful, unless we are automatically mapping an extension to a
# function.
def _check_read(fname):
    known_extensions = ['.edf', '.tiff', '.tif', '.h5', '.hdf', '.npy', '.nc', '.xrm',
                        '.txrm', '.txm', '.xmt']
    if not isinstance(fname, six.string_types):
        logger.error('File name must be a string')
    else:
        if writer.get_extension(fname) not in known_extensions:
            logger.error('Unknown file extension')
    return os.path.abspath(fname)


def read_tiff(fname, slc=None):
    """
    Read data from tiff file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Output 2D image.
    """
    fname = _check_read(fname)
    try:
        arr = tifffile.imread(fname, out='memmap')
    except IOError:
        logger.error('No such file or directory: %s', fname)
        return False
    arr = _slice_array(arr, slc)
    _log_imported_data(fname, arr)
    return arr


def read_tiff_stack(fname, ind, digit=None, slc=None):
    """
    Read data from stack of tiff files in a folder.

    Parameters
    ----------
    fname : str
        One of the file names in the tiff stack.
    ind : list of int
        Indices of the files to read.
    digit : int
        (Deprecated) Number of digits used in indexing stacked files.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Output 3D image.
    """
    fname = _check_read(fname)
    list_fname = _list_file_stack(fname, ind, digit)

    arr = _init_arr_from_stack(list_fname[0], len(ind), slc)
    for m, fname in enumerate(list_fname):
        arr[m] = read_tiff(fname, slc)
    _log_imported_data(fname, arr)
    return arr


def read_xrm(fname, slice_range=None):
    """
    Read data from xrm file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    slice_range : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Output 2D image.
    """
    fname = _check_read(fname)
    try:
        ole = olefile.OleFileIO(fname)
    except IOError:
        print('No such file or directory: %s', fname)
        return False

    metadata = read_ole_metadata(ole)

    if slice_range is None:
        slice_range = (slice(None), slice(None))
    else:
        slice_range = _make_slice_object_a_tuple(slice_range)

    stream = ole.openstream("ImageData1/Image1")
    data = stream.read()

    data_type = _get_ole_data_type(metadata)
    data_type = data_type.newbyteorder('<')

    arr = np.reshape(
        np.fromstring(data, data_type),
        (
            metadata["image_width"],
            metadata["image_height"]
        )
    )[slice_range]

    _log_imported_data(fname, arr)

    ole.close()
    return arr, metadata

#  Should slc just take over what ind is doing here?
def read_xrm_stack(fname, ind, slc=None):
    """
    Read data from stack of xrm files in a folder.

    Parameters
    ----------
    fname : str
        One of the file names in the tiff stack.
    ind : list of int
        Indices of the files to read.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Output 3D image.
    """
    fname = _check_read(fname)
    list_fname = _list_file_stack(fname, ind)

    number_of_images = len(ind)
    arr, metadata = _init_ole_arr_from_stack(
        list_fname[0], number_of_images, slc)
    del metadata["thetas"][0]
    del metadata["x_positions"][0]
    del metadata["y_positions"][0]

    for m, fname in enumerate(list_fname):
        arr[m], angle_metadata = read_xrm(fname, slc)
        metadata["thetas"].append(angle_metadata["thetas"][0])
        metadata["x_positions"].append(angle_metadata["x_positions"][0])
        metadata["y_positions"].append(angle_metadata["y_positions"][0])

    _log_imported_data(fname, arr)
    return arr, metadata


def read_aps_1id_metafile(metafn):
    """
    Parse log file generated at APS 1-ID

    Parameters
    ----------
    metafn : str
        Path to metafile of the experiment

    Returns
    -------
    dataframe
        Metadata stored as Pandas DataFrame.
    """
    # use pandas to organize metadata
    with open(metafn) as f:
        rawlines = f.readlines()

    # locate each layer
    # - each layer much have a head start with "Beginning of tomography"
    # - failed layer does not contain "End of the full scan"
    scan_head_ln = [i for i, line in enumerate(rawlines) 
                      if "Beginning of tomography" in line] + [len(rawlines)]
    layers_lns = list(zip(scan_head_ln[0:-1], scan_head_ln[1:]))
    layers_isValid = [ ( "End of the full scan" in "".join(rawlines[lns[0]:lns[1]]) ) 
                       for i, lns in enumerate(layers_lns)]
    
    # parse each layer into DataFrames
    dfs = []
    for layerID, lns in enumerate(layers_lns):
        # skip over the incomplete layer
        if not layers_isValid[layerID]: continue

        # prep for current layer
        layer_rawlines = rawlines[lns[0]:lns[1]]
        cycled_imgtypes = cycle(['pre_white', 
                                 'still', 
                                 'post_white', 
                                 'post_dark',
                                 ])

        # iterate through each line
        for i in range(len(layer_rawlines)):
            ln = layer_rawlines[i]

            # the format of the metadata file requires hard coding...
            if "num    nSeq" not in ln:
                # layer meta?
                # -- metastr seems important, so I keep the whole string for 
                #    each individual img for now
                #    However, this is definitely not a good practice in the 
                #    long run.
                if ":" in ln:
                    entry_key = ln.split(":")[0]
                    entry = ":".join(ln.split(":")[1:]).strip()
                    if entry_key.lower() == 'Path'.lower():
                        path = entry
                    elif entry_key.lower() == 'Image prefix'.lower():
                        prefix = entry
                    elif entry_key.lower() == "Energy (keV)".lower():
                        energy = float(entry)
                    elif entry_key.lower() == "New omega position".lower():
                        image_type = next(cycled_imgtypes)
                    elif entry_key.lower() == "tomo_metastr".lower():
                        tomo_metastr = entry
                    else:
                        continue
            else:
                # this is the start of an image meta info block
                block_start = i
                while(True):
                    i = i+1
                    if layer_rawlines[i] == "\n":
                        block_end = i
                        break
                # construct a dataframe from the block 
                # -- the date time column contains single white space, which 
                #    makes it impossible to directly use white space as the 
                #    delimenator.  Here we replace all 2+ white space with 
                #    tab so that later Pandas can easily identify each column
                image_block = [re.sub("  +", "\t", line.strip()) 
                               for line in layer_rawlines[block_start:block_end]]

                # construct the dataframe
                df = pd.read_csv(StringIO("\n".join(image_block)), sep='\t')
                # -- having layerID makes it easier to see what went wrong 
                #    during the experiment by directly locating the corrupted 
                #    layer
                df['layerID']     = layerID  
                df['path']        = path
                df['energy(kev)'] = energy
                df['prefix']      = prefix
                df['type']        = image_type
                df['metastr']     = tomo_metastr
                # now convert the time to datetime object
                df['Date'] = pd.to_datetime(df['Date'], 
                                            infer_datetime_format=True,
                                           )

                dfs.append(df)
                
    return pd.concat(dfs, ignore_index=True)


def read_txrm(file_name, slice_range=None):
    """
    Read data from a .txrm file, a compilation of .xrm files.

    Parameters
    ----------
    file_name : str
        String defining the path of file or file name.
    slice_range : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Array of 2D images.

    dictionary
        Dictionary of metadata.
    """
    file_name = _check_read(file_name)
    try:
        ole = olefile.OleFileIO(file_name)
    except IOError:
        print('No such file or directory: %s', file_name)
        return False

    metadata = read_ole_metadata(ole)

    array_of_images = np.empty(
        _shape_after_slice(
            (
                metadata["number_of_images"],
                metadata["image_height"],
                metadata["image_width"],
            ),
            slice_range
        ),
        dtype=np.float32
    )

    if slice_range is None:
        slice_range = (slice(None), slice(None), slice(None))
    else:
        slice_range = _make_slice_object_a_tuple(slice_range)

    for i in range(*slice_range[0].indices(metadata["number_of_images"])):
        img_string = "ImageData{}/Image{}".format(
            int(np.ceil((i + 1) / 100.0)), int(i + 1))
        array_of_images[i] = _read_ole_image(ole, img_string, metadata)[slice_range[1:]]

    reference = metadata['reference']
    if reference is not None:
        metadata['reference'] = reference[slice_range[1:]]

    _log_imported_data(file_name, array_of_images)

    ole.close()
    return array_of_images, metadata


def read_txm(file_name, slice_range=None):
    """
    Read data from a .txm file, the reconstruction file output
    by Zeiss software.

    Parameters
    ----------
    file_name : str
        String defining the path of file or file name.
    slice_range : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Array of 2D images.

    dictionary
        Dictionary of metadata.
    """

    return read_txrm(file_name, slice_range)


def read_ole_metadata(ole):
    """
    Read metadata from an xradia OLE file (.xrm, .txrm, .txm).

    Parameters
    ----------
    ole : OleFileIO instance
        An ole file to read from.

    Returns
    -------
    tuple
        A tuple of image metadata.
    """

    number_of_images = _read_ole_value(ole, "ImageInfo/NoOfImages", "<I")

    metadata = {
        'facility': _read_ole_value(ole, 'SampleInfo/Facility', '<50s'),
        'image_width': _read_ole_value(ole, 'ImageInfo/ImageWidth', '<I'),
        'image_height': _read_ole_value(ole, 'ImageInfo/ImageHeight', '<I'),
        'data_type': _read_ole_value(ole, 'ImageInfo/DataType', '<1I'),
        'number_of_images': number_of_images,
        'pixel_size': _read_ole_value(ole, 'ImageInfo/pixelsize', '<f'),
        'reference_filename': _read_ole_value(ole, 'ImageInfo/referencefile', '<260s'),
        'reference_data_type': _read_ole_value(ole, 'referencedata/DataType', '<1I'),   
        # NOTE: converting theta to radians from degrees
        'thetas': _read_ole_arr(
            ole, 'ImageInfo/Angles', "<{0}f".format(number_of_images)) * np.pi / 180.,
        'x_positions': _read_ole_arr(
            ole, 'ImageInfo/XPosition', "<{0}f".format(number_of_images)),
        'y_positions': _read_ole_arr(
            ole, 'ImageInfo/YPosition', "<{0}f".format(number_of_images)),
        'x-shifts': _read_ole_arr(
            ole, 'alignment/x-shifts', "<{0}f".format(number_of_images)),
        'y-shifts': _read_ole_arr(
            ole, 'alignment/y-shifts', "<{0}f".format(number_of_images))
    }
    # special case to remove trailing null characters
    reference_filename = _read_ole_value(ole, 'ImageInfo/referencefile', '<260s')
    if reference_filename is not None:
        for i in range(len(reference_filename)):
            if reference_filename[i] == '\x00':
                #null terminate
                reference_filename = reference_filename[:i]
                break
    metadata['reference_filename'] = reference_filename
    if ole.exists('referencedata/image'):
        reference = _read_ole_image(ole, 'referencedata/image', metadata, metadata['reference_data_type'])
    else:
        reference = None
    metadata['reference'] = reference
    return metadata


def _log_imported_data(fname, arr):
    logger.debug('Data shape & type: %s %s', arr.shape, arr.dtype)
    logger.info('Data successfully imported: %s', fname)


def _init_arr_from_stack(fname, number_of_files, slc):
    """
    Initialize numpy array from files in a folder.
    """
    _arr = read_tiff(fname, slc)
    size = (number_of_files, _arr.shape[0], _arr.shape[1])
    logger.debug('Data initialized with size: %s', size)
    return np.empty(size, dtype=_arr.dtype)


def _init_ole_arr_from_stack(fname, number_of_files, slc):
    """
    Initialize numpy array from files in a folder.
    """
    _arr, metadata = read_xrm(fname, slc)
    size = (number_of_files, _arr.shape[0], _arr.shape[1])
    logger.debug('Data initialized with size: %s', size)
    return np.empty(size, dtype=_arr.dtype), metadata


def _get_ole_data_type(metadata, datatype=None):
    # 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
    if datatype is None:
        datatype = metadata["data_type"]
    if datatype == 10:
        return np.dtype(np.float32)
    elif datatype == 5:
        return np.dtype(np.uint16)
    else:
        raise Exception("Unsupport XRM datatype: %s" % str(datatype))


def read_edf(fname, slc=None):
    """
    Read data from edf file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Data.
    """
    try:
        fname = _check_read(fname)
        f = EdfFile.EdfFile(fname, access='r')
        d = f.GetStaticHeader(0)
        arr = np.empty((f.NumImages, int(d['Dim_2']), int(d['Dim_1'])))
        for i in range(arr.shape[0]):
            arr[i::] = f.GetData(i)
        arr = _slice_array(arr, slc)
    except KeyError:
        logger.error('Unrecognized EDF data format')
        arr = None
    _log_imported_data(fname, arr)
    return arr


def read_dx_dims(fname, dataset):
    """
    Read array size of a specific group of Data Exchange file.
    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.
    Returns
    -------
    ndarray
        Data set size.
    """

    grp = '/'.join(['exchange', dataset])

    with h5py.File(fname, "r") as f:
        try:
            data = f[grp]
        except KeyError:
            return None

        shape = data.shape

    return shape

def read_hdf5(fname, dataset, slc=None, dtype=None, shared=False):
    """
    Read data from hdf5 file from a specific group.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.
    dtype : numpy datatype (optional)
        Convert data to this datatype on read if specified.
    shared : bool (optional)
        If True, read data into shared memory location.  Defaults to True.

    Returns
    -------
    ndarray
        Data.
    """
    try:
        fname = _check_read(fname)
        with h5py.File(fname, "r") as f:
            try:
                data = f[dataset]
            except KeyError:
                # NOTE: I think it would be better to raise an exception here.
                logger.error('Unrecognized hdf5 dataset: "%s"' %
                             (str(dataset)))
                return None
            shape = _shape_after_slice(data.shape, slc)
            if dtype is None:
                dtype = data.dtype
            if shared:
                arr = empty_shared_array(shape, dtype)
            else:
                arr = np.empty(shape, dtype)
            data.read_direct(arr, _make_slice_object_a_tuple(slc))
    except KeyError:
        return None
    _log_imported_data(fname, arr)
    return arr


def read_netcdf4(fname, group, slc=None):
    """
    Read data from netcdf4 file from a specific group.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    group : str
        Variable name where data is stored.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Data.
    """
    fname = _check_read(fname)
    f = netCDF4.Dataset(fname, 'r')
    try:
        arr = f.variables[group]
    except KeyError:
        f.close()
        logger.error('Unrecognized netcdf4 group')
        return None
    arr = _slice_array(arr, slc)
    f.close()
    _log_imported_data(fname, arr)
    return arr


def read_npy(fname, slc=None):
    """
    Read binary data from a ``.npy`` file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Data.
    """
    fname = _check_read(fname)
    arr = np.load(fname)
    arr = _slice_array(arr, slc)
    _log_imported_data(fname, arr)
    return arr


def read_spe(fname, slc=None):
    """
    Read data from spe file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    slc : sequence of tuples, optional
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Data.
    """
    fname = _check_read(fname)
    f = spefile.PrincetonSPEFile(fname)
    arr = f.getData()
    arr = _slice_array(arr, slc)
    _log_imported_data(fname, arr)
    return arr


def _make_slice_object_a_tuple(slc):
    """
    Fix up a slc object to be tuple of slices.
    slc = None returns None
    slc is container and each element is converted into a slice object

    Parameters
    ----------
    slc : None or sequence of tuples
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.
    """
    if slc is None:
        return None  # need arr shape to create slice
    fixed_slc = list()
    for s in slc:
        if not isinstance(s, slice):
            # create slice object
            if s is None or isinstance(s, int):
                # slice(None) is equivalent to np.s_[:]
                # numpy will return an int when only an int is passed to
                # np.s_[]
                s = slice(s)
            else:
                s = slice(*s)
        fixed_slc.append(s)
    return tuple(fixed_slc)


def read_fits(fname, fixdtype=True):
    """
    Read data from fits file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.

    Returns
    -------
    ndarray
        Data.
    """
    # NOTE:
    # at astropy 1.0.5, it is necessary to fix the dtype
    # but at 1.1.1, it seems unnecessary
    def _getDataType(path):
        bitpix = _readBITPIX(path)
        if bitpix > 0:
            dtype = 'uint%s' % bitpix
        elif bitpix <= -32:
            dtype = 'float%s' % -bitpix
        else:
            dtype = 'int%s' % -bitpix
        return dtype

    def _readBITPIX(path):
        # astropy fits reader has a problem
        # have to read BITPIX from the fits file directly
        stream = open(path, 'rb')
        while True:
            line = stream.read(80).decode("utf-8")
            if line.startswith('BITPIX'):
                value = line.split('/')[0].split('=')[1].strip()
                value = int(value)
                break
            continue
        stream.close()
        return value

    from astropy.io import fits
    f = fits.open(fname)
    arr = f[0].data
    f.close()
    if fixdtype:
        dtype = _getDataType(fname)
        if dtype:
            arr = np.array(arr, dtype=dtype)
    _log_imported_data(fname, arr)
    return arr


def _slice_array(arr, slc):
    """
    Perform slicing on ndarray.

    Parameters
    ----------
    arr : ndarray
        Input array to be sliced.
    slc : sequence of tuples
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Sliced array.
    """
    if slc is None:
        logger.debug('No slicing applied to image')
        return arr[:]
    axis_slice = _make_slice_object_a_tuple(slc)
    logger.debug('Data sliced according to: %s', axis_slice)
    return arr[axis_slice]


def _shape_after_slice(shape, slc):
    """
    Return the calculated shape of an array after it has been sliced.
    Only handles basic slicing (not advanced slicing).

    Parameters
    ----------
    shape : tuple of ints
        Tuple of ints defining the ndarray shape
    slc : tuple of slices
        Object representing a slice on the array.  Should be one slice per
        dimension in shape.

    """
    if slc is None:
        return shape
    new_shape = list(shape)
    slc = _make_slice_object_a_tuple(slc)
    for m, s in enumerate(slc):
        # indicies will perform wrapping and such for the shape
        start, stop, step = s.indices(shape[m])
        new_shape[m] = int(math.ceil((stop - start) / float(step)))
        if new_shape[m] < 0:
            new_shape[m] = 0
    return tuple(new_shape)


def _list_file_stack(fname, ind, digit=None):
    """
    Return a stack of file names in a folder as a list.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    ind : list of int
        Indices of the files to read.
    digit : int
        Deprecated input for the number of digits in all indexes
        of the stacked files.
    """

    if digit is not None:
        warnings.warn(("The 'digit' argument is deprecated and no longer used."
                      "  It may be removed completely in a later version."),
                      FutureWarning)

    body = writer.get_body(fname)
    body, digits = writer.remove_trailing_digits(body)

    ext = writer.get_extension(fname)
    list_fname = []
    for m in ind:
        counter_string = str(m).zfill(digits)
        list_fname.append(body + counter_string + ext)
    return list_fname


@contextmanager
def find_dataset_group(fname):
    """
    Finds the group name containing the stack of projections datasets within
    an ALS BL8.3.2 hdf5 file  containing a stack of images

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.

    Returns
    -------
    h5py.Group
    """
    with h5py.File(fname, 'r') as h5object:
        yield _find_dataset_group(h5object)


def _find_dataset_group(h5object):
    """
    Finds the group name containing the stack of projections datasets within
    an ALS BL8.3.2 hdf5 file  containing a stack of images
    """

    # Only one root key means only one dataset in BL8.3.2 current format
    keys = list(h5object.keys())
    if len(keys):
        if isinstance(h5object[keys[0]], h5py.Group):
            group_keys = list(h5object[keys[0]].keys())
            if isinstance(h5object[keys[0]][group_keys[0]], h5py.Dataset):
                return h5object[keys[0]]
            else:
                return _find_dataset_group(h5object[keys[0]])
        else:
            raise Exception('HDF5 Group with dataset stack not found')
    else:
        raise Exception('HDF5 Group with dataset stack not found')


def _count_proj(group, dname, nproj, digit=4, inter_bright=None):
    """
    Count the number of projections that have a specified name structure.
    Used to count the number of brights or darks in ALS BL8.3.2 hdf5 files when
    number is not present in metadata.
    """

    body = os.path.splitext(dname)[0]
    body = ''.join(body[:-digit])

    regex = re.compile('.*(' + body + ').*')
    count = len(list(filter(regex.match, list(group.keys()))))

    if inter_bright > 0:
        count = count / (nproj / inter_bright + 2)
    elif inter_bright == 0:
        count = count / 2

    return int(count)


def _map_loc(ind, loc):
    """
    Does a linear mapping of the indices where brights where taken within the
    full tomography to new indices of only those porjections which where read
    The returned list of indices is used in normalize_nn function.
    """

    loc = np.array(loc)
    low, upp = ind[0], ind[-1]
    buff = (loc[-1] - loc[0]) / len(loc)
    min_loc = low - buff
    max_loc = upp + buff
    loc = np.intersect1d(loc[loc > min_loc], loc[loc < max_loc])
    new_upp = len(ind) - 1
    loc = (new_upp * (loc - low)) // (upp - low)
    if loc[0] < 0:
        loc[0] = 0

    return np.ndarray.tolist(loc)


def _read_ole_struct(ole, label, struct_fmt):
    """
    Reads the struct associated with label in an ole file
    """
    value = None
    if ole.exists(label):
        stream = ole.openstream(label)
        data = stream.read()
        value = struct.unpack(struct_fmt, data)
    return value


def _read_ole_value(ole, label, struct_fmt):
    """
    Reads the value associated with label in an ole file
    """
    value = _read_ole_struct(ole, label, struct_fmt)
    if value is not None:
        value = value[0]
    return value


def _read_ole_arr(ole, label, struct_fmt):
    """
    Reads the numpy array associated with label in an ole file
    """
    arr = _read_ole_struct(ole, label, struct_fmt)
    if arr is not None:
        arr = np.array(arr)
    return arr


def _read_ole_image(ole, label, metadata, datatype=None):
    stream = ole.openstream(label)
    data = stream.read()
    data_type = _get_ole_data_type(metadata, datatype)
    data_type = data_type.newbyteorder('<')
    image = np.reshape(
        np.fromstring(data, data_type),
        (metadata["image_height"], metadata["image_width"], )
    )
    return image


def read_hdf5_stack(h5group, dname, ind, digit=4, slc=None, out_ind=None):
    """
    Read data from stacked datasets in a hdf5 file

    Parameters
    ----------

    fname : str
        One of the dataset names in the dataset stack

    ind : list of int
        Indices of the datasets to be read

    digit : int
        (Deprecated) Number of digits indexing the stacked datasets

    slc : {sequence, int}
        Range of values for slicing data.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix

    out_ind : list of int, optional
        Outer level indices for files with two levels of indexing.
        i.e. [name_000_000.tif, name_000_001.tif, ..., name_000_lmn.tif,
        name_001_lmn.tif, ..., ..., name_fgh_lmn.tif]
    """

    list_fname = _list_file_stack(dname, ind, digit)

    if out_ind is not None:
        list_fname_ = []
        for name in list_fname:
            fname = (writer.get_body(name).split('/')[-1] + '_' + digit * '0' +
                     writer.get_extension(name))
            list_fname_.extend(_list_file_stack(fname, out_ind, digit))
        list_fname = sorted(list_fname_, key=lambda x: str(x).split('_')[-1])

    for m, image in enumerate(list_fname):
        _arr = h5group[image]
        _arr = _slice_array(_arr, slc)
        if m == 0:
            dx, dy, dz = _arr.shape
            dx = len(list_fname)
            arr = np.empty((dx, dy, dz), dtype=_arr.dtype)
        arr[m] = _arr

    return arr

def read_file_list(file_list):
    """
    Read data from stack of image files in a folder.

    Parameters
    ----------

    file_list : list of str
        List of file names to read, in order
    """
    
    f = file_list[0]
    try:
        readfunc = tifffile.imread
        im = readfunc(f)
    except ValueError:
        readfunc = functools.partial(sm.imread, flatten=True)
        im = readfunc(f)
    
    if len(im.shape) != 2:
        raise ValueError('Only 2D images are supported in read_file_list')

    arr = np.zeros((len(file_list), im.shape[0], im.shape[1]), dtype=im.dtype)

    arr[0] = im
    for i, fn in enumerate(file_list[1:]):
        arr[i+1] = readfunc(fn)
    
    return arr
