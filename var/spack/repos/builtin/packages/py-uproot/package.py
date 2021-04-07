# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUproot(PythonPackage):
    """ROOT I/O in pure Python and NumPy

    Uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, Uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, Uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://uproot4.readthedocs.io"
    git      = "https://github.com/scikit-hep/uproot4"
    url      = "https://github.com/scikit-hep/uproot4/archive/0.0.27.tar.gz"

    maintainers = ['vvolkl']

    tags = ['hep']

    version('master', branch='master')
    version('4.0.6', sha256='1bea2ccc899c6959fb2af69d7e5d1e2df210caab30d3510e26f3fc07c143c37e')
    version('4.0.2', sha256='8145af29788cbe6bf0ee279a7f176159f3eee801641ead4ad6e627f8c4dff0a9')
    version('0.1.2', sha256='b32dbffadc87bc5707ee0093964d2ce4a5ccfd521b17bbf10732afc25b820d82')
    version('0.0.27', sha256='de87555937332998b476f3e310392962bc983bddc008ed2b3c07a25c0379c4c9')

    variant('xrootd', default=True,
            description='Build with xrootd support ')
    variant('lz4', default=True,
            description='Build with support for reading '
                        'lz4-compressed rootfiles ')

    variant('zstd', default=True,
            description='Build with support for reading '
                        'zstd-compressed rootfiles ')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    depends_on('xrootd', when="+xrootd")

    depends_on('lz4', when="+lz4")
    depends_on('xxhash', when="+lz4")

    depends_on('zstd', when="+zstd")
