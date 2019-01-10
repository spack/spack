# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyH5glance(PythonPackage):
    """H5Glance lets you explore HDF5 files in the terminal or
    an HTML interface.
    """

    homepage = "https://github.com/European-XFEL/h5glance"
    url      = "https://pypi.io/packages/source/h/h5glance/h5glance-0.4.tar.gz"

    version('0.4', sha256='03babaee0d481991062842796126bc9e6b11e2e6e7daba57c26f2b58bf3bbd32')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-python-htmlgen', type='run')
