# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://pypi.python.org/pypi/argcomplete"
    url      = "https://pypi.io/packages/source/a/argcomplete/argcomplete-1.1.1.tar.gz"

    version('1.1.1', '89a3839096c9f991ad33828e72d21abf')

    depends_on('py-setuptools', type='build')
