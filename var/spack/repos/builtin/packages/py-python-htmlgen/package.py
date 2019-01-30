# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPythonHtmlgen(PythonPackage):
    """Library to generate HTML from classes.
    """

    homepage = "https://github.com/srittau/python-htmlgen"
    url      = "https://github.com/srittau/python-htmlgen/archive/v1.2.2.tar.gz"

    version('1.2.2', sha256='9dc60e10511f0fd13014659514c6c333498c21779173deb585cd4964ea667770')

    conflicts('python@3.0:3.3.99')

    depends_on('py-setuptools', type='build')
    # dependencies for tests
    depends_on('py-typing', type='test')
    depends_on('py-python-asserts', type='test')
