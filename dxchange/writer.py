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
Module for data exporting data files.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import dxchange.dtype as dt
import numpy as np
import os
import six
import h5py
import logging
import re
from itertools import cycle

__author__ = "Doga Gursoy, Francesco De Carlo"
__copyright__ = "Copyright (c) 2015-2016, UChicago Argonne, LLC."
__version__ = "0.1.0"
__docformat__ = 'restructuredtext en'
__all__ = ['write_dxf',
           'write_hdf5',
           'write_npy',
           'write_tiff',
           'write_tiff_stack',
           'write_vtr',
           'write_aps_1id_report',
           ]

logger = logging.getLogger(__name__)


def _check_import(modname):
    try:
        return __import__(modname)
    except ImportError:
        logger.warn('Warning: ' + modname + ' module not found')
        return None

dxfile = _check_import('dxfile')


def get_body(fname):
    """
    Get file name after extension removed.
    """
    body = os.path.splitext(fname)[0]
    return body


def get_extension(fname):
    """
    Get file extension.
    """
    return '.' + fname.split(".")[-1]


def remove_trailing_digits(text):
    digit_string = re.search('\d+$', text)
    if digit_string is not None:
        number_of_digits = len(digit_string.group())
        text = ''.join(text[:-number_of_digits])
        return (text, number_of_digits)
    else:
        return (text, 0)


def _init_dirs(fname):
    """
    Initialize directories for saving output files.

    Parameters
    ----------
    fname : str
        Output file name.
    """
    dname = os.path.dirname(os.path.abspath(fname))
    if not os.path.exists(dname):
        os.makedirs(dname)


def _suggest_new_fname(fname, digit):
    """
    Suggest new string with an attached (or increased) value indexing
    at the end of a given string.

    For example if "myfile.tiff" exist, it will return "myfile-1.tiff".

    Parameters
    ----------
    fname : str
        Output file name.
    digit : int, optional
        Number of digits in indexing stacked files.

    Returns
    -------
    str
        Indexed new string.
    """
    if os.path.isfile(fname):
        body = get_body(fname)
        ext = get_extension(fname)
        indq = 1
        file_exist = False
        while not file_exist:
            fname = body + '-' + '{0:0={1}d}'.format(indq, digit) + ext
            if not os.path.isfile(fname):
                file_exist = True
            else:
                indq += 1
    return fname


def _init_write(arr, fname, ext, dtype, overwrite):
    if not (isinstance(fname, six.string_types)):
        fname = 'tmp/data' + ext
    else:
        if not fname.endswith(ext):
            fname = fname + ext
    fname = os.path.abspath(fname)
    if not overwrite:
        fname = _suggest_new_fname(fname, digit=1)
    _init_dirs(fname)
    if dtype is not None:
        arr = dt.as_dtype(arr, dtype)
    return fname, arr


def _write_hdf5_dataset(h5object, data, dname, appendaxis, maxshape):
    """
    Create a dataset and write data to a specific hdf5 object
    (file or group).

    Parameters
    ----------
    h5object: h5py object
        hdf5 object to write the dataset to.
    data : ndarray
        Array data to be saved.
    dname : str
        dataset name
    appendaxis : int
        Axis of dataset to which data will be appended.
        If given will create a resizable dataset.
    maxshape: tuple
        maxshape of resizable dataset.
        Only used if dataset has not been created.
    """
    if appendaxis is not None:
        if dname not in h5object:
            h5object.create_dataset(dname, data=data,
                                    maxshape=maxshape)
        else:
            size = h5object[dname].shape
            newsize = list(size)
            newsize[appendaxis] += data.shape[appendaxis]
            h5object[dname].resize(newsize)

            slices = 3 * [slice(None, None, None), ]
            slices[appendaxis] = slice(size[appendaxis], None, None)
            h5object[dname][tuple(slices)] = data
    else:
        h5object.create_dataset(dname, data=data)


def write_hdf5(
        data, fname='tmp/data.h5', gname='exchange', dname='data',
        dtype=None, overwrite=False, appendaxis=None, maxsize=None):
    """
    Write data to hdf5 file in a specific group.

    Parameters
    ----------
    data : ndarray
        Array data to be saved.
    fname : str
        File name to which the data is saved. ``.h5`` extension
        will be appended if it does not already have one.
    gname : str, optional
        Path to the group inside hdf5 file where data will be written.
    dname : str, optional
        Name for dataset where data will be written.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    overwrite: bool, optional
        if True, overwrites the existing file if the file exists.
    appendaxis: int, optional
        Axis where data is to be appended to.
        Must be given when creating a resizable dataset.
    maxsizee: int, optional
        Maximum size that the dataset can be resized to along the
        given axis.
    """
    mode = 'w' if overwrite else 'a'

    if appendaxis is not None:
        overwrite = True  # True if appending to file so fname is not changed
        maxshape = list(data.shape)
        maxshape[appendaxis] = maxsize
    else:
        maxshape = maxsize
    fname, data = _init_write(data, fname, '.h5', dtype, overwrite)

    with h5py.File(fname, mode=mode) as f:
        if 'implements' not in f:
            f.create_dataset('implements', data=gname)
        if gname not in f:
            f.create_group(gname)
        _write_hdf5_dataset(f[gname], data, dname,
                            appendaxis, maxshape)


def write_dxf(
        data, fname='tmp/data.h5', axes='theta:y:x',
        dtype=None, overwrite=False):
    """
    Write data to a data exchange hdf5 file.

    Parameters
    ----------
    data : ndarray
        Array data to be saved.
    fname : str
        File name to which the data is saved. ``.h5`` extension
        will be appended if it does not already have one.
    axes : str
        Attribute labels for the data array axes.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    overwrite: bool, optional
        if True, overwrites the existing file if the file exists.
    """
    fname, data = _init_write(data, fname, '.h5', dtype, overwrite)
    f = dxfile.dxtomo.File(fname, mode='w')
    f.add_entry(dxfile.dxtomo.Entry.data(data={
                'value': data, 'units': 'counts',
                'description': 'transmission', 'axes': axes}))
    f.close()


def write_npy(
        data, fname='tmp/data.npy', dtype=None, overwrite=False):
    """
    Write data to a binary file in NumPy ``.npy`` format.

    Parameters
    ----------
    data : ndarray
        Array data to be saved.
    fname : str
        File name to which the data is saved. ``.npy`` extension
        will be appended if it does not already have one.
    """
    fname, data = _init_write(data, fname, '.npy', dtype, overwrite)
    np.save(fname, data)


def write_tiff(
        data, fname='tmp/data.tiff', dtype=None, overwrite=False):
    """
    Write image data to a tiff file.

    Parameters
    ----------
    data : ndarray
        Array data to be saved.
    fname : str
        File name to which the data is saved. ``.tiff`` extension
        will be appended if it does not already have one.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    overwrite: bool, optional
        if True, overwrites the existing file if the file exists.
    """
    fname, data = _init_write(data, fname, '.tiff', dtype, overwrite)
    import tifffile
    tifffile.imsave(fname, data)


def write_tiff_stack(
        data, fname='tmp/data.tiff', dtype=None, axis=0, digit=5,
        start=0, overwrite=False):
    """
    Write data to stack of tiff file.

    Parameters
    ----------
    data : ndarray
        Array data to be saved.
    fname : str
        Base file name to which the data is saved. ``.tiff`` extension
        will be appended if it does not already have one.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    axis : int, optional
        Axis along which stacking is performed.
    start : int, optional
        First index of file in stack for saving.
    digit : int, optional
        Number of digits in indexing stacked files.
    overwrite: bool, optional
        if True, overwrites the existing file if the file exists.
    """
    fname, data = _init_write(data, fname, '.tiff', dtype, True)
    body = get_body(fname)
    ext = get_extension(fname)
    _data = np.swapaxes(data, 0, axis)
    for m in range(start, start + data.shape[axis]):
        _fname = body + '_' + '{0:0={1}d}'.format(m, digit) + ext
        if not overwrite:
            _fname = _suggest_new_fname(_fname, digit=1)
        write_tiff(_data[m - start], _fname, overwrite=overwrite)


def write_vtr(data, fname='tmp/data.vtr', down_sampling=(5, 5, 5)):
    """
    Write the reconstructed data (img stackes) to vtr file (retangular grid)

    Parameters
    ----------
    data          :  np.3darray
        reconstructed 3D image stacks with axis=0 as the omega
    fname         :  str
        file name of the output vtr file
    down_sampling :  tuple 
        down sampling steps along three axes

    Returns
    -------
    None
    """
    # vtk is only used here, therefore doing an in module import
    import vtk
    from vtk.util import numpy_support
    
    # convert to unit8 can significantly reduce the output vtr file
    # size, or just do a severe down-sampling
    data = _normalize_imgstacks(data[::down_sampling[0], 
                                     ::down_sampling[1], 
                                     ::down_sampling[2],]) * 255
    
    # --init rectangular grid
    rGrid = vtk.vtkRectilinearGrid()
    coordArray = [vtk.vtkDoubleArray(),
                  vtk.vtkDoubleArray(),
                  vtk.vtkDoubleArray(),
                 ]
    coords = np.array([np.arange(data.shape[i]) for i in range(3)])
    coords = [0.5 * np.array([3.0 * coords[i][0] - coords[i][0 + int(len(coords[i]) > 1)]] + \
                             [coords[i][j-1] + coords[i][j] for j in range(1,len(coords[i]))] + \
                             [3.0 * coords[i][-1] - coords[i][-1 - int(len(coords[i]) > 1)]]
                            ) 
              for i in range(3)
             ]
    grid = np.array(list(map(len,coords)),'i')
    rGrid.SetDimensions(*grid)
    for i,points in enumerate(coords):
        for point in points:
            coordArray[i].InsertNextValue(point)

    rGrid.SetXCoordinates(coordArray[0])
    rGrid.SetYCoordinates(coordArray[1])
    rGrid.SetZCoordinates(coordArray[2])
    
    # vtk requires x to be the fast axis
    # NOTE:
    #    Proper coordinate transformation is required to connect the 
    #    tomography data with other down-stream analysis (such as FF-HEDM
    #    and NF-HEDM).
    imgstacks = np.swapaxes(data, 0, 2)
    
    VTKarray = numpy_support.numpy_to_vtk(num_array=imgstacks.flatten().astype(np.uint8),
                                          deep=True,
                                          array_type=vtk.VTK_UNSIGNED_CHAR,
                                         )
    VTKarray.SetName('img')
    rGrid.GetCellData().AddArray(VTKarray)
    
    rGrid.Modified()
    if vtk.VTK_MAJOR_VERSION <= 5: 
        rGrid.Update()

    # output to file
    writer = vtk.vtkXMLRectilinearGridWriter()
    writer.SetFileName(fname)
    writer.SetDataModeToBinary()
    writer.SetCompressorTypeToZLib()
    if vtk.VTK_MAJOR_VERSION <= 5: 
        writer.SetInput(rGrid)
    else:                          
        writer.SetInputData(rGrid)
    writer.Write()


def write_aps_1id_report(df_scanmeta, reportfn):
    """
    Generate report of beam conditions based on given DataFrame of the 
    metadata

    Parameters
    ----------
    df_scanmeta  :  pd.DataFrame
        DataFrame of the parsed metadata
            dxreader.read_aps_1id_metafile(log_file)
    reportfn     :  str
        Output report file name (include path)

    Returns
    -------
    pd.DataFrame
        Updated Dataframe with added beam conditions
    """
    import matplotlib.pyplot as plt

    # add calculation of four beam quality
    # -- Temporal Beam Stability
    df_scanmeta['TBS'] = df_scanmeta['IC-E3']/df_scanmeta['IC-E3'].values[0]
    # -- Vertical Beam Stability
    df_scanmeta['VBS'] = df_scanmeta['IC-E1']/df_scanmeta['IC-E2']
    # -- Beam Loss at Slit
    df_scanmeta['BLS'] = (df_scanmeta['IC-E1'] + df_scanmeta['IC-E2'])/df_scanmeta['IC-E3']
    # -- Beam Loss during Travel 
    df_scanmeta['BLT'] = df_scanmeta['IC-E5']/df_scanmeta['IC-E3']
    # -- corresponding color code
    pltlbs  = ['TBS',  'VBS',     'BLS', 'BLT' ]
    pltclrs = ['red', 'blue', 'magenta', 'cyan']

    # start plot
    fig = plt.figure(figsize=(8,3))
    ax  = fig.add_subplot(111)
    lnclrs = cycle(['gray', 'lime', 'gray', 'black'])
    # -- plot one segment at a time
    for lb, clr in zip(pltlbs, pltclrs):
        addlabel=True
        for layerID in df_scanmeta['layerID'].unique():
            tmpdf = df_scanmeta[df_scanmeta['layerID'] == layerID]
            for imgtype in tmpdf['type'].unique():
                # plot the main curve
                currentSlice = tmpdf[tmpdf['type'] == imgtype]

                ax.plot(currentSlice['Date'], currentSlice[lb], 
                        linewidth=0.2, 
                        color=clr,
                        label=lb if addlabel else '_nolegend_',
                        alpha=0.5,
                        )
                addlabel = False
                # add the vertical guard
                tmpx = currentSlice['Date'].values
                tmpclr = next(lnclrs)
                for x in [tmpx[0], tmpx[-1]]:
                    ax.plot([x, x], [1e-4, 1e2], 
                            color=tmpclr,
                            linewidth=0.05,
                            linestyle='dashed',
                            alpha=0.1,
                           )
    # -- set canvas property
    ax.set_yscale('log')
    plt.legend(loc=0)
    plt.ylim([0.9, 2.0])  # 10% as cut range
    plt.xticks(rotation=45)
    # -- save the figure (both pdf and png)
    plt.savefig(reportfn, 
                transparent=True, 
                bbox_inches='tight', 
                pad_inches=0.1,
               )
    # -- clear/close figure
    plt.close()
    
    return df_scanmeta


def _normalize_imgstacks(img):
    """
    Normalize image stacks on a per layer base

    Parameters
    ----------
    img  :  np.3darray
        img stacks to be normalized
    
    Returns
    -------
    np.3darray
        normalized image stacks
    """
    return img/np.amax(img.reshape(img.shape[0], 
                                   img.shape[1]*img.shape[2],
                                  ), 
                       axis=1,
                      ).reshape(img.shape[0],1,1)