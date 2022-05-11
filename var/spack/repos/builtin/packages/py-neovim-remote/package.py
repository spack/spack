# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyNeovimRemote(PythonPackage):
    """Remote opening and control for neovim: nvr"""

    homepage = "https://github.com/mhinz/neovim-remote"
    pypi     = "neovim-remote/neovim-remote-2.4.0.tar.gz"

    maintainers = ['trws']

    version('2.4.0', sha256='f199ebb61c3decf462feed4e7d467094ed38d8afaf43620736b5983a12fe2427')

    depends_on('python@3.5:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-pynvim', type=('build', 'run'))
