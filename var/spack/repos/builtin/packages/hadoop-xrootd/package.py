# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HadoopXrootd(MavenPackage):
    """Connector between Hadoop and XRootD protocols (EOS compatible)."""

    homepage = "https://gitlab.cern.ch/db/hadoop-xrootd"
    url      = "https://lcgpackages.web.cern.ch/tarFiles/sources/hadoop-xrootd-v1.0.7.tar.gz"

    maintainers = ['haralmha']

    version('1.0.7', sha256='9a129dc14b3dc139aa4da7543f6392a5c80b41fea6bb9f6cd27db5acf6f5471f')

    depends_on('hadoop')
    depends_on('xrootd')

    def build_args(self):
        return [
                '-Dxrootd.include.path={0}/include/xrootd'.format(self.spec['xrootd'].prefix)
                ]
