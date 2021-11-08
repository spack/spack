# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    pypi = "snakemake/snakemake-3.11.2.tar.gz"

    version('5.10.0', sha256='a3fa8b12db84938c919996d61be66031bcb99c4b4d017278731324a6112b0d59')
    version('5.6.0', sha256='65b944bcf06fd31b5da7430a6012a542c4c3c05a822b92ca218f2406eabd2c24')
    version('3.11.2', sha256='f7a3b586bc2195f2dce4a4817b7ec828b6d2a0cff74a04e0f7566dcd923f9761')

    depends_on('python@3.3:')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-appdirs', type='run')
    depends_on('py-configargparse', type='run')
    depends_on('py-datrie', type='run')
    depends_on('py-docutils', type='run')
    depends_on('py-gitpython', type='run')
    depends_on('py-jsonschema', type='run')
    depends_on('py-pyyaml', type='run')
    depends_on('py-ratelimiter', type='run')
    depends_on('py-requests', type='run')
    depends_on('py-wrapt', type='run')

    depends_on('py-nbformat', type='run', when='@5.10.0:')
    depends_on('py-psutil', type='run', when='@5.10.0:')
    depends_on('py-toposort', type='run', when='@5.10.0:')
