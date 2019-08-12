# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDxfile(PythonPackage):
    """Scientific Data Exchange [A1] is a set of guidelines for storing scientific
       data and metadata in a Hierarchical Data Format 5 [B6] file."""

    homepage = "https://github.com/data-exchange/dxfile"
    url      = "https://github.com/data-exchange/dxfile/archive/v0.4.tar.gz"

    import_modules = ['dxfile']

    version('0.4', '0402cd38aefdfd5ce92feb43dda18947')

    depends_on('py-setuptools', type='build')
    depends_on('py-h5py', type=('build', 'run'))
