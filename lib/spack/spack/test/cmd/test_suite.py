##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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
import pytest
import spack.cmd.test_suite as test_suite
import datetime
import os
import unittest


@pytest.mark.usefixtures('config')
class TestCompilers(object):

    def test_filename(self):
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        assert "test.yaml" in ts.yaml_file

    def test_combinatorial(self):
        combinations = []
        compiler = "gcc"
        versions = ["4.2.1", "6.3.0"]
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        [combinations.append(spec)
         for spec in ts.combinatorial(compiler, versions)]
        assert len(combinations) == 2

    def test_combinatorial_compiler(self):
        combinations = []
        compiler_version = ["gcc@4.2.1", "gcc@6.3.0"]
        package_versions = ["bzip2@1.2.3", "libelf@3.4"]
        ts = test_suite.CombinatorialSpecSet("test.yaml")
        [combinations.append(spec)
         for spec in ts.combinatorial_compiler(
            compiler_version, package_versions)]
        assert len(combinations) == 4

    def test_create_path(self):
        test_suite.create_path()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        path = os.getcwd() + "/spack-test-" + str(timestamp) + "/"
        assert os.path.exists(path)
