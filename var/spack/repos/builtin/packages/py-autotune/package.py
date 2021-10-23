# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter


class PyAutotune(PythonPackage):
    """
    Common interface for autotuning search space and method definition
    """

    homepage = "https://github.com/ytopt-team/autotune"
    git      = "https://github.com/ytopt-team/autotune.git"

    version('master', branch='master')

    # depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    patch('problem.patch')

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
