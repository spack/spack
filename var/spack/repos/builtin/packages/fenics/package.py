# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Fenics(Package):
    """FEniCS is a popular open-source (LGPLv3) computing platform for
    solving partial differential equations (PDEs). FEniCS enables users
    to quickly translate scientific models into efficient finite element
    code. With the high-level Python and C++ interfaces to FEniCS, it is
    easy to get started, but FEniCS offers also powerful capabilities
    for more experienced programmers. FEniCS runs on a multitude of
    platforms ranging from laptops to high-performance clusters."""

    homepage = "https://fenicsproject.org/"

    # Dummy url, remove when metapackage/bundlepackage is available
    url      = 'file://' + os.path.dirname(__file__) + '/README.md'

    version('2018.1.0', sha256='39272696b633f9336895df1267ef35568b62cf0b68c18d292bc9662a926993de', expand=False)

    depends_on('fenics-dolfin+python')
    depends_on('fenics-mshr+python')

    depends_on('py-fenics-dijitso')
    depends_on('py-fenics-ffc')
    depends_on('py-fenics-fiat')
    depends_on('py-fenics-ufl')

    # Dummy install, remove when metapackage/bundlepackage is available
    def install(self, spec, prefix):
        install('README.md', prefix)
