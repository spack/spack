# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMmtf(PythonPackage):
    """A decoding libary for the PDB mmtf format."""

    homepage = "https://pypi.org/project/mmtf-python"
    url      = "https://files.pythonhosted.org/packages/13/ea/c6a302ccdfdcc1ab200bd2b7561e574329055d2974b1fb7939a7aa374da3/mmtf-python-1.1.2.tar.gz"

    version('1.1.2', sha256='a5caa7fcd2c1eaa16638b5b1da2d3276cbd3ed3513f0c2322957912003b6a8df')

    extends('python@2.7:')
    depends_on('py-setuptools', type='build')

