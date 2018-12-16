# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Meson(PythonPackage):
    """Meson is a portable open source build system meant to be both
       extremely fast, and as user friendly as possible."""

    homepage = "http://mesonbuild.com/"
    url      = "https://github.com/mesonbuild/meson/archive/0.49.0.tar.gz"

    version('0.49.0', sha256='11bc959e7173e714e4a4e85dd2bd9d0149b0a51c8ba82d5f44cc63735f603c74')
    version('0.42.0', '9e26bf154ca439b78b1b9366c8a89437')
    version('0.41.2', 'aa9c69ced965e47f5c75a9257ee91ce3')
    version('0.41.1', 'c6d285b35cfd7acc8517124d417efbdc')

    variant('ninjabuild', default=True)

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('ninja', when='+ninjabuild', type=('build', 'run'))
