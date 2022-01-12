# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFindlibs(PythonPackage):
    """A package to search for shared libraries on various platforms."""

    homepage = "https://github.com/ecmwf/findlibs"
    pypi     = "findlibs/findlibs-0.0.2.tar.gz"

    version('0.0.2', sha256='6c7e038496f9a97783ab2cd5736bb68522d5bebd8b0eb17c976b6a4ae4032c8d')

    depends_on('py-setuptools', type='build')
