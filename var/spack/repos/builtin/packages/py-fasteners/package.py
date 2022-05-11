# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyFasteners(PythonPackage):
    """A python package that provides useful locks."""

    homepage = "https://github.com/harlowja/fasteners"
    pypi = "fasteners/fasteners-0.14.1.tar.gz"

    version('0.17.3', sha256='a9a42a208573d4074c77d041447336cf4e3c1389a256fd3e113ef59cf29b7980')
    version('0.16.3', sha256='b1ab4e5adfbc28681ce44b3024421c4f567e705cc3963c732bf1cba3348307de')
    version('0.14.1', sha256='427c76773fe036ddfa41e57d89086ea03111bbac57c55fc55f3006d027107e18')

    depends_on('python@3.6:', when='@0.17:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-monotonic@0.1:', when='@0.16 ^python@:3.3', type=('build', 'run'))
    depends_on('py-monotonic@0.1:',  when='@:0.15', type=('build', 'run'))
    depends_on('py-six', when='@:0.16', type=('build', 'run'))
