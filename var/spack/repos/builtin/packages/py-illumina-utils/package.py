# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIlluminaUtils(PythonPackage):
    """A library and collection of scripts to work with Illumina paired-end
    data (for CASAVA 1.8+)."""

    homepage = "https://github.com/meren/illumina-utils"
    pypi = "illumina-utils/illumina-utils-2.2.tar.gz"

    version('2.10',  sha256='720612ef2be2498af3327171e273284bf174a3f0b27efaded9f8ffcf323655e1')
    version('2.9',   sha256='fb45781ecc7075d7acf37d830a0cc56dfa8667cbd10c954478aedfa930031a34')
    version('2.8',   sha256='20b954cb883b763f42336dd4ff8f8ee3fda09d4b0667068542fb48c364f1bf53')
    version('2.7',   sha256='f4308291e93721d20bdcf78e3bf152618b0a015e044c22bbcf68b4cae68f61f2')
    version('2.6',   sha256='4ee7108d6ae67fc7d6c70bee4f775d38dfd921c10e4b020bd177838c649446ea')
    version('2.5',   sha256='664f2c6a003afe4d424b5b16a14344e320dce3e226d6f8970b5abc65297aed44')
    version('2.4.1', sha256='a006cb66279f526b1627954022f032a43fc6500904894c40a0c814ffafa2e5b4')
    version('2.4',   sha256='8bbab8e70f70e3a212f6bff9532c77bd3ceca02312acb042a98895e531cc7c49')
    version('2.3', sha256='0e8407b91d530d9a53d8ec3c83e60f25e7f8f80d06ce17b8e4f57a02d3262441')
    version('2.2', sha256='6039c72d077c101710fe4fdbfeaa30caa1c3c2c84ffa6295456927d82def8e6d')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-python-levenshtein', type=('build', 'run'))
