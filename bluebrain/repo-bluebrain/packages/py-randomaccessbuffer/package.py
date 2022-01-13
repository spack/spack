# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRandomaccessbuffer(PythonPackage):
    """This repository contains the Python codec for RandomAccessBuffer
    (RAB) file format.
    RAB is a container format, rather generic but originally thought for
    containing scientific datasets where precision and integrity matters.
    It is close to HDF5 and yet very far. It can handle multiple datasets
    with their metadata ubt contrary to HDF5 it is very easy to decode,
    even from within a web browser in JS.
    """
    homepage = "https://bbpgitlab.epfl.ch/dke/randomaccessbufferpy"
    git      = "git@bbpgitlab.epfl.ch:dke/randomaccessbufferpy.git"

    version('0.1.7', tag='v0.1.7')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pytest-cov', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
