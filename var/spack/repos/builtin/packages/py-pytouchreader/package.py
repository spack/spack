# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyPytouchreader(PythonPackage):
    """Python interface to interact with touch files."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/PyModules"
    git      = "ssh://bbpcode.epfl.ch/hpc/PyModules"

    version('develop', clean=False)
    version('1.4.1', tag='v1.4.1', clean=False, preferred=True)
    version('1.4.0', tag='v1.4.0', clean=False)
    version('1.3.0', tag='v1.3.0', clean=False)
    version('1.2.0', tag='v1.2.0', clean=False)

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
            if not os.path.exists('.git'):
                os.symlink('../.git', '.git')
