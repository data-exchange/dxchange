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

import unittest
from dxchange import reader
import numpy as np
import os

TEST_DIR = os.path.dirname(os.path.dirname(__file__))


class read_files_test_case(unittest.TestCase):
    def test_read_xrm_reads_an_xrm_file(self):
        print(TEST_DIR)
        image_data, metadata = reader.read_xrm(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"), [1, 2])
        np.testing.utils.assert_(image_data is not False)
        np.testing.utils.assert_(metadata is not False)

    def test_read_txrm_reads_a_txrm_file(self):
        image_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"))
        np.testing.utils.assert_(image_data is not False)
        np.testing.utils.assert_(metadata is not False)

    def test_read_txrm_gets_metadata(self):
        image_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"))
        np.testing.utils.assert_(metadata["thetas"] is not False)
        np.testing.utils.assert_(metadata["x_positions"] is not False)
        np.testing.utils.assert_(metadata["y_positions"] is not False)

    def test_read_txrm_uses_slice_data(self):
        image_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"), (5, 128, 54))
        self.assertEqual(image_data.shape, (5, 128, 54))

    def test_read_txrm_works_on_a_list_of_slice_data(self):
        image_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"), [1, 2])
        self.assertEqual(image_data.shape, (1, 2, 256))

    def test_read_xrm_stack_reads_multiple_xrms(self):
        image_data, metadata = reader.read_xrm_stack(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"), [0, 1])
        np.testing.utils.assert_(image_data is not False)
        np.testing.utils.assert_(metadata is not False)

    # def test_read_hdf5():
    #     file_data = reader.read_hdf5("test/test_data/reader.h5", [1,2])
    #     np.testing.utils.assert_(file_data is not False)

    def test_read_xrm_gets_theta(self):
        array_data, metadata = reader.read_xrm(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"))
        self.assertEqual(metadata["thetas"], [-0.06000000238418579])

    def test_read_xrm_gets_x_position(self):
        array_data, metadata = reader.read_xrm(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"))
        self.assertEqual(metadata["x_positions"], [715.3599853515625])

    def test_read_xrm_gets_y_position(self):
        array_data, metadata = reader.read_xrm(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"))
        self.assertEqual(metadata["y_positions"], [-3761.9892578125])

    # def test_read_xrm_handles_ref_image():
    #     array_data, theta = reader.read_xrm(
    #         "test/test_data/test_flat.xrm", [1, 2])
    # Need a good flat ref test image

    def test_read_xrm_returns_properly_sliced_np_array_x_slice(self):
        image_data, metadata = reader.read_xrm(
            os.path.join(
                TEST_DIR,
                "test_data/test_chip00.xrm",
            ),
            ((0, 256), ),
        )
        self.assertEqual(
            image_data.shape,
            (256, 512, ),
        )

    def test_read_xrm_returns_properly_sliced_np_array_y_x_slice(self):
        image_data, metadata = reader.read_xrm(
            os.path.join(
                TEST_DIR,
                "test_data/test_chip00.xrm",
            ),
            ((0, 256), (384, 512), ),
        )
        self.assertEqual(
            image_data.shape,
            (256, 128, ),
        )

    def test_read_xrm_stack_gets_theta_set(self):
        image_data, metadata = reader.read_xrm_stack(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"), [0, 1])
        self.assertEqual(
            metadata["thetas"],
            [
                -0.06000000238418579,
                -0.06000000238418579,
            ]
        )

    def test_read_xrm_stack_gets_x_position_set(self):
        image_data, metadata = reader.read_xrm_stack(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"), [0, 1])
        self.assertEqual(
            metadata["x_positions"],
            [
                715.3599853515625,
                715.3599853515625,
            ]
        )

    def test_read_xrm_stack_gets_y_position_set(self):
        image_data, metadata = reader.read_xrm_stack(
            os.path.join(TEST_DIR, "test_data/test_chip00.xrm"), [0, 1])
        self.assertEqual(
            metadata["y_positions"],
            [
                -3761.9892578125,
                -3761.9892578125,
            ]
        )

    def test_read_txrm_gets_theta_set(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"))
        self.assertEqual(
            metadata["thetas"],
            [
                -45.018001556396484,
                -30.01412582397461,
                -15.01412582397461,
                -0.014125000685453415,
                14.985876083374023,
                29.985876083374023,
                44.985877990722656
            ]
        )

    def test_read_txrm_gets_x_position_set(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"))
        self.assertEqual(
            metadata["x_positions"],
            [
                1019.4400024414062,
                1019.4400024414062,
                1019.4599609375,
                1019.4400024414062,
                1019.4599609375,
                1019.4599609375,
                1019.4599609375,
            ]
        )

    def test_read_txrm_gets_y_position_set(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR, "test_data/txrm_test_chip_tomo.txrm"))
        self.assertEqual(
            metadata["y_positions"],
            [
                -3965.869384765625,
                -3965.889404296875,
                -3965.889404296875,
                -3965.889404296875,
                -3965.869384765625,
                -3965.869384765625,
                -3965.869384765625,
            ]
        )

    def test_read_txrm_returns_properly_sliced_np_array_x_slice(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR,
                "test_data/txrm_test_chip_tomo.txrm"
            ),
            ((0, 5), ),
        )
        self.assertEqual(
            array_data.shape,
            (5, 256, 256, )
        )

    def test_read_txrm_returns_properly_sliced_np_array_y_x_slice(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR,
                "test_data/txrm_test_chip_tomo.txrm"
            ),
            ((0, 5), (0, 128), ),
        )
        self.assertEqual(
            array_data.shape,
            (5, 128, 256, )
        )

    def test_read_txrm_returns_properly_sliced_np_array_z_y_x_slice(self):
        array_data, metadata = reader.read_txrm(
            os.path.join(
                TEST_DIR,
                "test_data/txrm_test_chip_tomo.txrm"
            ),
            ((0, 5), (0, 128), (59, 177), ),
        )
        self.assertEqual(
            array_data.shape,
            (5, 128, 118, )
        )

    def test_slice_array_does_not_slice_when_not_given_a_slice_range(self):
        test_array = [1, 2, 3]
        test_array = reader._slice_array(test_array, None)
        self.assertEqual(test_array, [1, 2, 3])

    def test_slice_array_slices_when_given_a_slice_range(self):
        test_array = reader._slice_array(
            np.array([[1, 2, 3], [1, 2, 3]]), [1, 2])
        np.testing.utils.assert_equal(test_array, np.array([[1, 2]]))


class shape_after_slice_test_case(unittest.TestCase):
    def test_it_should_return_shape_of_array_if_passed_none(self):
        shape = reader._shape_after_slice((2, 2), None)
        self.assertEqual((2, 2), shape)


class list_file_stack_test_case(unittest.TestCase):
    def test_list_file_stack_one_digit(self):
        file_stack = reader._list_file_stack("path/image_0.xrm", [1, 2])
        self.assertEqual(
            file_stack, ["path/image_1.xrm", "path/image_2.xrm"])

    def test_list_file_stack_five_digits(self):
        file_stack = reader._list_file_stack(
            "path/image_00000.xrm", [1, 2])
        self.assertEqual(
            file_stack,
            ["path/image_00001.xrm", "path/image_00002.xrm"])

    def test_list_file_stack_ten_digits(self):
        file_stack = reader._list_file_stack(
            "path/image_0000000000.xrm", [1, 2])
        self.assertEqual(
            file_stack,
            ["path/image_0000000001.xrm", "path/image_0000000002.xrm"])

    def test_list_file_stack_underscore_split_digits(self):
        file_stack = reader._list_file_stack(
            "path/image_00000_00000.xrm", [1, 2])
        self.assertEqual(
            file_stack,
            ["path/image_00000_00001.xrm", "path/image_00000_00002.xrm"])

    def test_list_file_stack_long_path(self):
        file_stack = reader._list_file_stack(
            "someFile/otherFile/image_0.xrm", [1, 2])
        self.assertEqual(
            file_stack,
            ["someFile/otherFile/image_1.xrm", "someFile/otherFile/image_2.xrm"])
