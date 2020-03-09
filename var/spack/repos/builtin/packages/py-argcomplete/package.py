# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://pypi.python.org/pypi/argcomplete"
    url      = "https://pypi.io/packages/source/a/argcomplete/argcomplete-1.1.1.tar.gz"

    version('1.1.1', sha256='cca45b5fe07000994f4f06a0b95bd71f7b51b04f81c3be0b4ea7b666e4f1f084')

    depends_on('py-setuptools', type='build')
