# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    url      = "https://pypi.io/packages/source/s/snakemake/snakemake-3.11.2.tar.gz"

    version('3.11.2', '6bf834526078522b38d271fdf73e6b22')

    depends_on('python@3.3:')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-wrapt', type=('build', 'run'))
