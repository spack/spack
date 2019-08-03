# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpython(PythonPackage):
    """IPython provides a rich toolkit to help you make the most out of using
       Python interactively."""
    homepage = "https://pypi.python.org/pypi/ipython"
    url      = "https://pypi.io/packages/source/i/ipython/ipython-2.3.1.tar.gz"

    version('7.3.0', '2aec01154a78c6075c5b7f1bfea4abd3')
    version('5.1.0', '47c8122420f65b58784cb4b9b4af35e3')
    version('3.1.0', 'a749d90c16068687b0ec45a27e72ef8f')
    version('2.3.1', '2b7085525dac11190bfb45bb8ec8dcbf')

    depends_on('python@2.7:2.8,3.3:')

    depends_on('py-backports-shutil-get-terminal-size', type=('build', 'run'), when="^python@:3.2")
    depends_on('py-pathlib2', type=('build', 'run'), when="^python@:3.3")
    depends_on('py-pygments',                   type=('build', 'run'))
    depends_on('py-pickleshare',                type=('build', 'run'))
    depends_on('py-simplegeneric@0.8:',         type=('build', 'run'))
    depends_on('py-prompt-toolkit@1.0.4:1.999', when='@:7.0.0', type=('build', 'run'))
    depends_on('py-prompt-toolkit@2.0.0:2.999', when='@7.0.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.2:',             type=('build', 'run'))
    depends_on('py-decorator',                  type=('build', 'run'))
    depends_on('py-pexpect',                    type=('build', 'run'))
    depends_on('py-backcall',                   type=('build', 'run'), when="^python@3.3:")
    depends_on('py-appnope', type=('build', 'run'), when='platform=darwin')

    conflicts('^python@2.7:2.8', when='@7.0.0:')
