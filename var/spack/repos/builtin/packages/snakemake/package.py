# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    pypi = "snakemake/snakemake-6.12.3.tar.gz"

    version('6.12.3', sha256='af86af9a540da3dceb05dad1040f1d3d733e6a695f8b3f8c30f8cf3bc6570a88')

    depends_on('python')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-wrapt', type=('build', 'run'))
    #newer versions
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-configargparse', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-datrie', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-docutils', type=('build', 'run'))
    depends_on('py-gitpython', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-toposort', type=('build', 'run'))
    depends_on('py-connectionpool@0.0.3:', type=('build', 'run'))
    depends_on('py-pulp@2.0:', type=('build', 'run'))
    depends_on('py-smart-open@3.0:', type=('build', 'run'))
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-stopit', type=('build', 'run'))
    depends_on('py-tabulate', type=('build', 'run'))
