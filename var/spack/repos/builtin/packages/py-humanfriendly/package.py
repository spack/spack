# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyHumanfriendly(PythonPackage):
    """Human friendly output for text interfaces using Python"""

    homepage = "https://pypi.org/project/humanfriendly/"
    url      = "https://files.pythonhosted.org/packages/26/71/e7daf57e819a70228568ff5395fdbc4de81b63067b93167e07825fcf0bcf/humanfriendly-4.18.tar.gz"

    version('4.18', sha256='33ee8ceb63f1db61cce8b5c800c531e1a61023ac5488ccde2ba574a85be00a85')

    depends_on('py-setuptools', type='build')
