# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyH5glance(PythonPackage):
    """H5Glance lets you explore HDF5 files in the terminal or an HTML interface."""

    homepage = "https://github.com/European-XFEL/h5glance"
    url      = "https://files.pythonhosted.org/packages/9e/15/0ab4dee0ee1cc7600ca39bde98194b122057542dde335d78251541d69cbd/h5glance-0.4.tar.gz"

    version('0.4', sha256='03babaee0d481991062842796126bc9e6b11e2e6e7daba57c26f2b58bf3bbd32')

    conflicts('python@:3.4.9') # python >= 3.5 is required
    depends_on('py-h5py', type=('build', 'run'))
