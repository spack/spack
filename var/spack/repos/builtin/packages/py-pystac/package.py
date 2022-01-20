# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPystac(PythonPackage):
    """Python library for working with Spatiotemporal Asset Catalog (STAC)."""

    homepage = "https://github.com/azavea/pystac.git"
    pypi     = "pystac/pystac-0.5.4.tar.gz"

    version('0.5.4', sha256='9fc3359364685adf54e3bc78c87550a8bc8b0a927405419bd8e4bbd42a8efc79')

    depends_on('py-setuptools', type='build')
    depends_on('py-python-dateutil@2.7.0:', type=('build', 'run'))
