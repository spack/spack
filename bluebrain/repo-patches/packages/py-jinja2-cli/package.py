# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJinja2Cli(PythonPackage):
    """A CLI interface to Jinja2"""

    homepage = "https://github.com/mattrobenolt/jinja2-cli"
    url = "https://pypi.io/packages/source/j/jinja2-cli/jinja2-cli-0.6.0.tar.gz"

    version('0.6.0', sha256='4b1be17ce8a8f133df02205c3f0d3ebfc3a68e795d26987f846a2316636427b7', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-jinja2', type='run')
