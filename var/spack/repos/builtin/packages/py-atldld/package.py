# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "https://github.com/BlueBrain/Atlas-Download-Tools"
    url      = "https://files.pythonhosted.org/packages/7d/f1/4295504e63c441f3756ececd2fd6ee13c0d8e449529b92647a36dd8b7ef9/atldld-0.2.2.tar.gz"

    maintainers = ['EmilieDel', 'jankrepl', 'Stannislav']

    version('0.2.2', sha256='4bdbb9ccc8e164c970940fc729a10bf883a67035e8c636261913cecb351835d3')

    # Build dependencies
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    depends_on('py-pillow', type='run')
    depends_on('py-appdirs', type='run')
    depends_on('py-click', type='run')
    depends_on('py-matplotlib', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-opencv-python', type='run')
    depends_on('py-pandas', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-scikit-image', type='run')
