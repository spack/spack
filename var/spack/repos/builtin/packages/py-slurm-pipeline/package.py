# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySlurmPipeline(PythonPackage):
    """A Python class for scheduling SLURM jobs"""

    homepage = "https://github.com/acorg/slurm-pipeline"
    url      = "https://pypi.io/packages/source/s/slurm-pipeline/slurm-pipeline-1.1.13.tar.gz"

    version('2.0.9',  '7f97d2410db441081b79ac5c3395b8d0')
    version('1.1.13', 'd1f8c78a64718ec5e2e40ba1b6816017')

    depends_on('py-setuptools', type='build')
    # using open range although requirements*.txt give explicit versions
    # test dependencies are omitted, see #7681
    depends_on('py-six@1.10.0:', type=('build', 'run'), when='^python@:2.8')
