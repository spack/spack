# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGsutilFeedstock(PythonPackage):
    """A command line tool for interacting with cloud storage services."""

    homepage = "https://github.com/conda-forge/gsutil-feedstock"
    pypi     = "gsutil/gsutil-4.59.tar.gz"

    maintainers = ['dorton21']

    version('4.59', sha256='349e0e0b48c281659acec205917530ae57e2eb23db7220375f5add44688d3ddf')

    depends_on('py-setuptools', type=('build', 'run'))
