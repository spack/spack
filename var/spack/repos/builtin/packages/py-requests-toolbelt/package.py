# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRequestsToolbelt(PythonPackage):
    """A toolbelt of useful classes and functions to be used with
    python-requests"""

    homepage = "https://toolbelt.readthedocs.org/"
    url      = "https://github.com/requests/toolbelt/archive/0.8.0.tar.gz"

    version('0.8.0', 'de9bf7fbcc6ae341a5c4fd9f8912bcac')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.0.1:3.0.0', type=('build', 'run'))
