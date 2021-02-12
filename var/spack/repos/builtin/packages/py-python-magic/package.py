# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPythonMagic(PythonPackage):
    """A python wrapper for libmagic"""

    homepage = "https://github.com/ahupp/python-magic"
    pypi = "python-magic/python-magic-0.4.15.tar.gz"

    version('0.4.20', sha256='0cc52ccad086c377b9194014e3dbf98d94b194344630172510a6a3e716b47801')
    version('0.4.19', sha256='c11721314cad741bde0cb57e978c3789b8cdab11d5456ef5842b7e7529bd43f1')
    version('0.4.18', sha256='b757db2a5289ea3f1ced9e60f072965243ea43a2221430048fd8cacab17be0ce')
    version('0.4.17', sha256='adf74ea289dbc1960547abab0fd5a519c21e9dd9bd96d3c280c3ec5e842a1b09')
    version('0.4.15', sha256='f3765c0f582d2dfc72c15f3b5a82aecfae9498bd29ca840d72f37d7bd38bfcd5')

    depends_on('py-setuptools', type='build')
