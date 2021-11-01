# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import zipfile

from spack import *


class PyFlitCore(PythonPackage):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    url = "https://github.com/takluyver/flit/archive/refs/tags/3.3.0.tar.gz"
    maintainers = ['takluyver']

    version('3.3.0', sha256='f5340b268563dd408bf8e2df6dbc8d4d08bc76cdff0d8c7f8a4be94e5f01f22f')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))

    def build(self, spec, prefix):
        with working_dir('flit_core'):
            python('build_dists.py')

    def install(self, spec, prefix):
        wheel = glob.glob(os.path.join('flit_core', 'dist', '*.whl'))[0]
        with zipfile.ZipFile(wheel) as f:
            f.extractall(site_packages_dir)
