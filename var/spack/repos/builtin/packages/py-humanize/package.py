# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHumanize(PythonPackage):
    """Python package that contains humanization utilities"""

    homepage = "https://github.com/jmoiron/humanize"
    url      = "https://github.com/jmoiron/humanize.git"

    version('develop', git=url, branch='master')
    version('0.5.1', git=url, tag='0.5.1', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))
