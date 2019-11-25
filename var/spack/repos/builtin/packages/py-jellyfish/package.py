# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyJellyfish(PythonPackage):
    """a library for doing approximate and phonetic matching of strings."""

    homepage = "https://pypi.org/project/jellyfish/"
    url      = "https://pypi.io/packages/source/j/jellyfish/jellyfish-0.6.1.tar.gz"

    version('0.6.1', sha256='5104e45a2b804b48a46a92a5e6d6e86830fe60ae83b1da32c867402c8f4c2094')

    depends_on('py-setuptools', type='build')
