# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://github.com/kislyuk/argcomplete"
    pypi = "argcomplete/argcomplete-1.12.0.tar.gz"

    version('2.0.0',  sha256='6372ad78c89d662035101418ae253668445b391755cfe94ea52f1b9d22425b20')
    version('1.12.3', sha256='2c7dbffd8c045ea534921e63b0be6fe65e88599990d8dc408ac8c542b72a5445')
    version('1.12.0', sha256='2fbe5ed09fd2c1d727d4199feca96569a5b50d44c71b16da9c742201f7cc295c')
    version('1.1.1',  sha256='cca45b5fe07000994f4f06a0b95bd71f7b51b04f81c3be0b4ea7b666e4f1f084')

    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-importlib-metadata@0.23:4', when='@1.12.3: ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.23:3', when='@1.12.2 ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.23:2', when='@1.12.1 ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.23:1', when='@1.12.0 ^python@:3.7', type=('build', 'run'))
