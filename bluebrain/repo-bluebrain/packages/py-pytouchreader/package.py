# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytouchreader(PythonPackage):
    """Python interface to interact with touch files."""

    homepage = "https://bbpgitlab.epfl.ch/hpc/touchreader"
    git      = "git@bbpgitlab.epfl.ch:hpc/touchreader.git"

    version('develop', get_full_repo=True)
    version('1.4.7', tag='v1.4.7', get_full_repo=True)
    version('1.4.6', tag='v1.4.6', get_full_repo=True)
    version('1.4.5', tag='v1.4.5', get_full_repo=True)
    version('1.4.4', tag='v1.4.4', get_full_repo=True)
    version('1.4.3', tag='v1.4.3', get_full_repo=True)
    version('1.4.2', tag='v1.4.2', get_full_repo=True)
    version('1.4.0', tag='v1.4.0', get_full_repo=True)
    version('1.3.0', tag='v1.3.0', get_full_repo=True)
    version('1.2.0', tag='v1.2.0', get_full_repo=True)

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))
