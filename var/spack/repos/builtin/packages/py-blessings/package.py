# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBlessings(PythonPackage):
    """A nicer, kinder way to write to the terminal """
    homepage = "https://github.com/erikrose/blessings"
    url      = "https://pypi.io/packages/source/b/blessings/blessings-1.6.tar.gz"

    version('1.6', '4f552a8ebcd4982693c92571beb99394')

    depends_on('py-setuptools', type='build')
