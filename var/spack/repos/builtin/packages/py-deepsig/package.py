# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeepsig(PythonPackage):
    """"""

    homepage = "https://github.com/Kaleidophon/deep-significance"
    url      = "https://github.com/Kaleidophon/deep-significance/archive/refs/tags/v1.2.0.tar.gz"
    git      = "https://github.com/Kaleidophon/deep-significance.git"

    version('1.2.0', sha256='e9abfb33aad03dbf6b5351fa35f813f7a041edc0ef64c16ce537a65911903306')

    depends_on('python@3.5.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.19.5', type=('build', 'run'))
    depends_on('py-scipy@1.6.0', type=('build', 'run'))
    depends_on('py-tqdm@4.59.0', type=('build', 'run'))
    depends_on('py-joblib@1.0.1', type=('build', 'run'))
    depends_on('py-pandas@1.3.3', type=('build', 'run'))
    depends_on('py-dill@0.3.4', type=('build', 'run'))
