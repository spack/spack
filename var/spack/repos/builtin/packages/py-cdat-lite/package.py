# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyCdatLite(PythonPackage):
    """Cdat-lite is a Python package for managing and analysing climate
    science data. It is a subset of the Climate Data Analysis Tools (CDAT)
    developed by PCMDI at Lawrence Livermore National Laboratory."""

    homepage = "http://proj.badc.rl.ac.uk/cedaservices/wiki/CdatLite"
    url      = "https://pypi.io/packages/source/c/cdat-lite/cdat-lite-6.0.1.tar.gz"

    version('6.0.1', '6d5a6e86f15ce15291d25feab8793248')

    depends_on("netcdf")
    depends_on("python@2.5:2.8", type=('build', 'run'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    phases = ['install']

    def install(self, spec, prefix):
        """Install everything from build directory."""
        install_args = self.install_args(spec, prefix)
        # Combine all phases into a single setup.py command,
        # otherwise extensions are rebuilt without rpath by install phase:
        self.setup_py('build_ext', '--rpath=%s' % ":".join(self.rpath),
                      'build_py', 'build_scripts',
                      'install', *install_args)
