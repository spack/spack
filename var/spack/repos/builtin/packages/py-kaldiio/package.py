# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKaldiio(PythonPackage):
    """A pure python module for reading and writing kaldi ark files"""

    homepage = "https://github.com/nttcslab-sp/kaldiio"
    url      = "https://github.com/nttcslab-sp/kaldiio/archive/refs/tags/v2.17.2.zip"

    version('2.17.2',   sha256='2e929970d45902b8e4d31eac58d8476bd8eda5dba808033bfd1b3b764481287c')
    version('2.17.1',   sha256='e2b77d3d16de05e4f0b06283a9bdeea6cdc1dd3b1c490138ff9ce990187cef04')
    version('2.17.0',   sha256='4cb2c8cb44b3c2f8b19bbd08d48d478b954f39f2b37e1eb6ad61cf5480f7994f')
    version('2.16.0',   sha256='05c0102c87505945c5e5e09d736e3882422478bce0ace15a28b9a77b79278ea7')
    version('2.15.1',   sha256='45c2f7876b1d4996021d54e83848dfe208e4f9afa186c26d8fd8c18ce20cd920')
    version('2.15.0',   sha256='08a37e2d43254be031c6ed4ad1b16f3e60364f71d48234a6d71e5e6da44cc7f9')
    version('2.14.1',   sha256='4bd1d5a20492b76c4f43043d342a0d0b6829eb70f72a1ea953d84a4be8515dbc')
    version('2.14.0',   sha256='a24a1ca5392965b5e1e52d97c0f7755188e8ada88d56e347cbab402bf4cb7681')
    version('2.13.9',   sha256='76a0d2162941a91b6d3ffa4d484273d4db7b060c5c10a58d279aa213c7b846cf')

    depends_on('python@2.7:, 3.5:',     type=('build', 'run'))
    depends_on('py-setuptools',         type='build')
    depends_on('py-numpy',              type=('build', 'run'))
