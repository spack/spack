# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PySacremoses(PythonPackage):
    """LGPL MosesTokenizer in Python."""

    homepage = "https://github.com/alvations/sacremoses"
    url      = "https://pypi.io/packages/source/s/sacremoses/sacremoses-0.0.38.tar.gz"

    version('0.0.38', sha256='34dcfaacf9fa34a6353424431f0e4fcc60e8ebb27ffee320d57396690b712a3b')

    depends_on('py-setuptools', type='build')
    depends_on('py-regex', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-joblib', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
