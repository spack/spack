# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PySubmitit(PythonPackage):
    """Python toolbox for submitting jobs to Slurm."""

    homepage = "https://github.com/facebookincubator/submitit"
    pypi = "submitit/submitit-1.3.3.tar.gz"

    version('1.3.3', sha256='efaa77b2df9ea9ee02545478cbfc377853ddf8016bff59df6988bebcf51ffa7e')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-cloudpickle@1.2.1:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7.4.2:', type=('build', 'run'))
