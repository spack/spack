# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/BlueBrain/libsonata"
    url = "https://pypi.io/packages/source/l/libsonata/libsonata-0.0.2.tar.gz"

    version('0.0.2', sha256='ea6655d8f1cb79262b5c5ad613386e88635ff7a4745cf7ef5643fd3c59be9a55', preferred=True)

    depends_on('cmake@3.3:', type='build')
    depends_on('hdf5~mpi', type='build')

    depends_on('py-numpy@1.12:', type='run')
