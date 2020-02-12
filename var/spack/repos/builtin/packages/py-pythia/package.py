# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythia(PythonPackage):
    """Pythia refers to the Pyre framework and a collection of packages that
    interact with it, such as an interface to the ACIS solid modelling package.
    """

    homepage = "https://geodynamics.org/cig/software/pythia/"
    url      = "https://geodynamics.org/cig/software/github/pythia/v0.8.1.18/pythia-0.8.1.18.tar.gz"

    version('0.8.1.18', sha256='f6025e6d70046dc71e375eded3d731506f8dd79e2e53b7e1436754439dcdef1e')

    depends_on('python@:2', type=('build', 'run'))
    depends_on('py-merlin', type='build')
