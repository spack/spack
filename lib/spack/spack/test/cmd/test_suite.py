##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import datetime

from spack.cmd.test_suite import create_output_directory, valid_yaml_files
from spack.stage import Stage


def test_valid_yaml_files():
    with Stage('valid-yaml-files'):
        # create fake yaml file
        test_files = []
        test_files.append(os.getcwd() + "/test3.yaml")
        for file in test_files:
            if not os.path.exists(file):
                open(file, "a")

        assert len(valid_yaml_files(test_files)) == 1


def test_return_valid_yaml_file_list():
    with Stage('valid-yaml-file-list'):
        # create fake yaml file
        test_files = []
        test_files.append(os.getcwd() + "/test2.txt")
        test_files.append(os.getcwd() + "/test2.yaml")
        for file in test_files:
            if not os.path.exists(file):
                open(file, "a")

        assert len(valid_yaml_files(test_files)) == 1


def test_create_output_directory():
    with Stage('create-output-directory'):
        create_output_directory()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        path = os.getcwd() + "/spack-test-" + str(timestamp) + "/"
        assert os.path.exists(path)
