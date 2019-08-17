# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTifffile(PythonPackage):
    """Read and write image data from and to TIFF files."""

    homepage = "https://github.com/blink1073/tifffile"
    url      = "https://pypi.io/packages/source/t/tifffile/tifffile-0.12.1.tar.gz"

    import_modules = ['tifffile']

    version('0.12.1', '8a8afa74dd0df7915ac376a6cd7eeffc')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.8.2:', type=('build', 'run'))
