# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyHumanize(PythonPackage):
    """This modest package contains various common humanization utilities, like
    turning a number into a fuzzy human readable duration ('3 minutes ago') or
    into a human readable size or throughput. It works with python 2.7 and 3.3
    and is localized to Russian, French, Korean and Slovak.
    """

    homepage = "https://github.com/jmoiron/humanize"
    pypi = "humanize/humanize-0.5.1.tar.gz"

    version('4.0.0', sha256='ee1f872fdfc7d2ef4a28d4f80ddde9f96d36955b5d6b0dac4bdeb99502bddb00')
    version('3.12.0', sha256='5ec1a66e230a3e31fb3f184aab9436ea13d4e37c168e0ffc345ae5bb57e58be6')
    version('0.5.1', sha256='a43f57115831ac7c70de098e6ac46ac13be00d69abbf60bdcac251344785bb19')

    depends_on('python@3.7:', when='@4:', type=('build', 'run'))
    depends_on('python@3.6:', when='@3:', type=('build', 'run'))
    depends_on('python@3.5:', when='@1.1.0:', type=('build', 'run'))
    depends_on('python@2.7:2,3.5:', when='@1.0.0', type=('build', 'run'))
    depends_on('py-setuptools@42:', when='@3.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm+toml@3.4:', when='@3.2:', type='build')
    depends_on('py-setuptools-scm', when='@1:', type='build')
    depends_on('py-importlib-metadata', when='@3.12: ^python@:3.7', type=('build', 'run'))
