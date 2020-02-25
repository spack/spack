# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProgressbar(PythonPackage):
    """Text progress bar library for Python."""

    homepage = "https://github.com/niltonvolpato/python-progressbar"
    url      = "https://pypi.org/packages/source/p/progressbar/progressbar-2.5.tar.gz"

    version('2.5', sha256='5d81cb529da2e223b53962afd6c8ca0f05c6670e40309a7219eacc36af9b6c63')

    depends_on('py-setuptools', type='build')
