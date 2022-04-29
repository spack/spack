# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyAniso8601(PythonPackage):
    """A library for parsing ISO 8601 strings."""

    homepage = "https://bitbucket.org/nielsenb/aniso8601"
    pypi     = "aniso8601/aniso8601-9.0.1.tar.gz"

    version('9.0.1', sha256='72e3117667eedf66951bb2d93f4296a56b94b078a8a95905a052611fb3f1b973')

    depends_on('py-setuptools', type='build')
