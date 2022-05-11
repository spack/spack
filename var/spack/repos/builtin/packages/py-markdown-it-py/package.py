# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class PyMarkdownItPy(PythonPackage):
    """Markdown parser, done right.
       100% CommonMark support, extensions, syntax plugins & high speed """

    homepage = "https://github.com/executablebooks/markdown-it-py"
    git      = "https://github.com/executablebooks/markdown-it-py"
    pypi     = "markdown-it-py/markdown-it-py-1.1.0.tar.gz"

    version('1.1.0', sha256='36be6bb3ad987bfdb839f5ba78ddf094552ca38ccbd784ae4f74a4e1419fc6e3')

    depends_on('python@3.6:3',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-attrs@19:21', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4:', type=('build', 'run'), when='^python@:3.7')
