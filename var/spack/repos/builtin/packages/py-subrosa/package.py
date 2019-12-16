# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySubrosa(PythonPackage):
    """Subrosa is a Python implementation of Shamir's Secret Sharing. An
    algorithm for sharing a secret with a group of people without letting any
    individual of the group know the secret."""

    homepage = "https://github.com/DasIch/subrosa/"
    url      = "https://github.com/DasIch/subrosa/archive/0.1.0.tar.gz"

    version('0.1.0', '61c46944b9f7d039a37aef4bace60a3e')

    depends_on('py-setuptools', type='build')
    depends_on('py-gf256',        type=('build', 'run'))
