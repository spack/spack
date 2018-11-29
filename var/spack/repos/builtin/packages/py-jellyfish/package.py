# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyJellyfish(PythonPackage):
    """a library for doing approximate and phonetic matching of strings."""

    homepage = "https://pypi.org/project/jellyfish/"
    url      = "https://pypi.io/packages/source/j/jellyfish/jellyfish-0.6.1.tar.gz"

    version('0.6.1', '4944750af050995d38dd3c42709ae2ab')

    depends_on('py-setuptools', type='build')
