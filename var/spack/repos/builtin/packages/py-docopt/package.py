# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDocopt(PythonPackage):
    """Command-line interface description language."""

    homepage = "http://docopt.org/"
    url      = "https://pypi.io/packages/source/d/docopt/docopt-0.6.2.tar.gz"

    import_modules = ['docopt']

    version('0.6.2', '4bc74561b37fad5d3e7d037f82a4c3b1')

    depends_on('py-setuptools', type='build')
