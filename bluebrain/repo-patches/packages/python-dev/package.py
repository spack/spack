# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PythonDev(BundlePackage):
    """Meta package to bundle python packages for development"""

    homepage = "http://www.dummy.org/"
    url      = "https://www.dummy.org/source/dummy-0.2.zip"

    version('0.5')

    # Any new dependency here needs to have a comment as to _why_ it is required and
    # should be included here.  Otherwise the deployment team will feel free to remove it
    # as soon as it poses any issue.
    depends_on('python', type=('build', 'run'))
    depends_on('py-cmake-format', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-jinja2-cli', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-mariadb', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-sympy', type=('build', 'run'))

    def setup_run_environment(self, env):
        for dep in self.spec.dependencies(deptype='run'):
            env.prepend_path('PATH', dep.prefix.bin)
