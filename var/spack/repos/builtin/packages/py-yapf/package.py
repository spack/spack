# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYapf(PythonPackage):
    """ Yet Another Python Formatter """
    homepage = "https://github.com/google/yapf"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://github.com/google/yapf/archive/v0.2.1.tar.gz"

    version('0.2.1', '348ccf86cf2057872e4451b204fb914c')

    depends_on('py-setuptools', type='build')
