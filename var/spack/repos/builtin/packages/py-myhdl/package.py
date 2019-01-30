# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyMyhdl(PythonPackage):
    """Python as a Hardware Description Language"""

    homepage = "http://www.myhdl.org"
    url      = "https://pypi.io/packages/source/m/myhdl/myhdl-0.9.0.tar.gz"

    version('0.9.0', 'c3b4e7b857b6f51d43720413546df15c')

    depends_on('python@2.6:2.8,3.4:')
    depends_on('py-setuptools', type='build')
