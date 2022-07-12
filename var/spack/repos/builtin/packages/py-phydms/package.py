# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhydms(PythonPackage):
    """phydms enables phylogenetic analyses using deep mutational scanning data
       to inform the substitution models. It implements Experimentally informed
       codon models (ExpCM) for phylogenetic inference and the detection of
       biologically interesting selection."""

    homepage = "http://jbloomlab.github.io/phydms"
    pypi     = "phydms/phydms-2.4.1.tar.gz"

    version('2.4.1', sha256='04eb50bdb07907214050d19214d9bc8cf2002e24ca30fbe6e0f23f013d584d5c')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
