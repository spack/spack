# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXenv(PythonPackage):
    """Helpers to work with the environment in a platform independent way."""

    homepage = "https://gitlab.cern.ch/gaudi/xenv"
    git      = "https://gitlab.cern.ch/gaudi/xenv.git"

    # As of 0.0.4, all released versions of xenv corrupt the system environment
    # in a manner which breaks Spack's compiler wrappers. Therefore, we must
    # package an un-released development version of xenv.
    version('develop',            branch='master')
    version('develop_2018-12-20', commit='ddc3bf5e65e1689da499f639af7a27c5c4242841')

    depends_on('py-setuptools', type='build')
