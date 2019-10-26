# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class PyNbconvert(PythonPackage):
    """Jupyter Notebook Conversion"""

    homepage = "https://github.com/jupyter/nbconvert"
    url      = "https://github.com/jupyter/nbconvert/archive/4.2.0.tar.gz"

    version('4.2.0', sha256='32394be5a20f39f99fabfb9b2f2625df17f1c2a6699182ca41598e98e7cc9610')
    version('4.1.0', sha256='459f23381411fd1ff9ec5ed71fcd56b8c080d97b3a1e47dae1c5c391f9a47266')
    version('4.0.0', sha256='00e25eeca90523ba6b774b289073631ef5ac65bb2de9774e9b7f29604516265c')

    depends_on('py-pycurl', type='build')
    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-mistune', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-entrypoints', type=('build', 'run'))
    depends_on('py-tornado', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))

    def patch(self):
        # We bundle this with the spack package so that the installer
        # doesn't try to download it.
        install(os.path.join(self.package_dir, 'style.min.css'),
                os.path.join('nbconvert', 'resources', 'style.min.css'))
