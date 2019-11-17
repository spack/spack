# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWub(PythonPackage):
    """Bioinformatics tools and a software library developed by the Oxford
    Nanopore Technologies Applications group.
    """

    homepage = "https://github.com/nanoporetech/wub"
    url      = "https://github.com/nanoporetech/wub/archive/v0.4.0.tar.gz"

    version('0.4.0', sha256='1526aa392bccac71b872211c45f5b403ad3d55f5762e0ed34ff9086bc1dab6fd')

    depends_on('py-six')
    depends_on('py-pytest', type=('build', 'test'))
    depends_on('py-pycmd', type=('build', 'run', 'test'))
    depends_on('py-biopython')
    depends_on('py-numpy', type=('build', 'run', 'test'))
    depends_on('py-matplotlib')
    depends_on('py-seaborn')
    depends_on('py-editdistance', type=('build', 'run', 'test'))
    depends_on('py-pandas@0.20.2:')
    depends_on('py-pysam')
    depends_on('py-tqdm')
    depends_on('py-statsmodels')
    depends_on('py-setuptools')
