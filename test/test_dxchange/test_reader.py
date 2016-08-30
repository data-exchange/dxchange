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

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy
from dxchange import reader
import os


THIS_DIR = os.path.dirname(os.path.dirname(__file__))

def test_read_xrm_reads_an_xrm_file():
    image_data, theta = reader.read_xrm(os.path.join(THIS_DIR, "test_data/test_chip00.xrm"), [1,2])
    numpy.testing.utils.assert_(image_data is not False)
    numpy.testing.utils.assert_(theta is not False)
    
    
def test_read_txrm_reads_a_txrm_file():
    image_data, thetas = reader.read_txrm(os.path.join(THIS_DIR, "test_data/txrm_test_chip_tomo.txrm"), [1,2])
    numpy.testing.utils.assert_(image_data is not False)
    numpy.testing.utils.assert_(thetas is not False)
    
def test_read_xrm_stack_reads_multiple_xrms():
    image_data, thetas = reader.read_xrm_stack(os.path.join(THIS_DIR, "test_data/test_chip00.xrm"), [0,1])
    numpy.testing.utils.assert_(image_data is not False)
    numpy.testing.utils.assert_(thetas is not False)
    
#def test_read_hdf5():
#    file_data = reader.read_hdf5("test/test_data/reader.h5", [1,2])
#    numpy.testing.utils.assert_(file_data is not False)

def test_read_xrm_gets_theta():
    array_data, theta = reader.read_xrm(os.path.join(THIS_DIR, "test_data/test_chip00.xrm"), [1,2])
    numpy.testing.utils.assert_equal(theta, -0.06000000238418579)
    
#def test_read_xrm_handles_ref_image():
#    array_data, theta = reader.read_xrm("test/test_data/test_flat.xrm", [1,2])
# Need a good flat ref test image  
  
def test_read_xrm_stack_gets_theta_set():
    image_data, thetas = reader.read_txrm(os.path.join(THIS_DIR, "test_data/txrm_test_chip_tomo.txrm"), [1,2])
    numpy.testing.utils.assert_equal(thetas, (-45.018001556396484, 
                                              -30.01412582397461, 
                                              -15.01412582397461, 
                                              -0.014125000685453415, 
                                              14.985876083374023, 
                                              29.985876083374023, 
                                              44.985877990722656)
)

    
def test_read_txrm_gets_theta_set():
    array_data, thetas = reader.read_txrm(os.path.join(THIS_DIR, "test_data/txrm_test_chip_tomo.txrm"), [1,2])
    numpy.testing.utils.assert_equal(thetas, (-45.018001556396484, 
                                              -30.01412582397461,
                                              -15.01412582397461, 
                                              -0.014125000685453415, 
                                              14.985876083374023, 
                                              29.985876083374023, 
                                              44.985877990722656))

def test_slice_array_does_not_slice_when_not_given_a_slice_range():
    test_array = [1,2,3]
    test_array = reader._slice_array(test_array, None)
    numpy.testing.utils.assert_equal(test_array, [1,2,3])
    
def test_slice_array_slices_when_given_a_slice_range():
    test_array = reader._slice_array(numpy.array([[1,2,3,],[1,2,3]]),[1,2])
    numpy.testing.utils.assert_equal(test_array, numpy.array([[1,2]]))
    
def test_list_file_stack_one_digit():
    file_stack = reader._list_file_stack("path/image_0.xrm", [1,2])
    numpy.testing.utils.assert_equal(file_stack, ["path/image_1.xrm", "path/image_2.xrm"])

def test_list_file_stack_five_digits():
    file_stack = reader._list_file_stack("someFile/someOtherFile/imageOfSorts_00000.xrm", [1,2])
    numpy.testing.utils.assert_equal(file_stack, ["someFile/someOtherFile/imageOfSorts_00001.xrm", "someFile/someOtherFile/imageOfSorts_00002.xrm"])

def test_list_file_stack_ten_digits():
    file_stack = reader._list_file_stack("path/image_0000000000.xrm", [1,2])
    numpy.testing.utils.assert_equal(file_stack, ["path/image_0000000001.xrm", "path/image_0000000002.xrm"])
    
if __name__ == '__main__':
    import nose
    nose.runmodule(exit=False)