# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoconf(PythonPackage):
    """moconf is a package for configuring a Morpheus appliance."""

    homepage = "https://pypi.org/project/moconf/#files"
    pypi     = "moconf/moconf-0.0.18.tar.gz"

    maintainers = ['dorton21']

    version('0.0.18', sha256='a39c68d7416854a7655111da78d0f000333bab371d26ab1f2dee80166b28b614')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.21.0:', type='build')
    depends_on('py-urllib3', type='build')
