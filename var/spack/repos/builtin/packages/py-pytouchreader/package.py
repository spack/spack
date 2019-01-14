# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyPytouchreader(PythonPackage):
    """Python interface to interact with touch files."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/PyModules"
    url      = "ssh://bbpcode.epfl.ch/hpc/PyModules"

    version('develop', git=url, clean=False)
    version('1.2.0', tag='v1.2.0', git=url, clean=False, preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-lazy-property', type=('build', 'run'))

    build_directory = 'PyTouchReader'

    @run_before('build')
    def link_git(self):
        """Link the git directory into the local directory

        Needed for `setuptools_scm` to work.
        """
        with working_dir(self.build_directory):
            os.symlink('../.git', '.git')
