# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMikado(PythonPackage):
    """Mikado is a lightweight Python3 pipeline whose purpose is to facilitate
       the identification of expressed loci from RNA-Seq data * and to select
       the best models in each locus."""

    homepage = "https://github.com/EI-CoreBioinformatics/mikado"
    url = "https://pypi.io/packages/source/M/Mikado/Mikado-1.2.4.tar.gz"

    version('1.2.4', sha256='c0485dba3b7c285599809e058c83f33b5efa9522d20d9f980423410604207f61')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-wheel@0.28.0:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-jsonschema@3.0.1:', type=('build', 'run'))
    depends_on('py-numpy@1.16.0:', type=('build', 'run'))
    depends_on('py-networkx@2:', type=('build', 'run'))
    depends_on('py-sqlalchemy@1.3:', type=('build', 'run'))
    depends_on('py-sqlalchemy-utils', type=('build', 'run'))
    depends_on('py-biopython@1.78:', type=('build', 'run'))
    depends_on('py-intervaltree', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('py-pyfaidx', type=('build', 'run'))
    depends_on('py-scikit-learn@0.17.0:', type=('build', 'run'))
    depends_on('py-scipy@1.0.0:', type=('build', 'run'))
    depends_on('py-drmaa', type=('build', 'run'))
    depends_on('snakemake', type=('build', 'run'))
    depends_on('py-docutils@0.13.2:', type=('build', 'run'))
    depends_on('py-tabulate', type=('build', 'run'))
    depends_on('py-msgpack@1.0.0:', type=('build', 'run'))
    depends_on('py-python-rapidjson@0.8:', type=('build', 'run'))
    depends_on('py-pandas@:1.1.5', type=('build', 'run'))
    depends_on('py-jsonref', type=('build', 'run'))
    depends_on('py-pysam@0.15.3:', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-tomlkit', type=('build', 'run'))
