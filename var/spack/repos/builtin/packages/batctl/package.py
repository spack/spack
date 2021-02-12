# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Batctl(MakefilePackage):
    """B.A.T.M.A.N. advanced control and management tool"""

    homepage = "https://github.com/open-mesh-mirror/batctl"
    url      = "https://github.com/open-mesh-mirror/batctl/archive/v2019.5.tar.gz"

    version('2021.0', sha256='9cec8bf1952f885192749a9dc0318a54633b717aaf05c438d504efd83f5201e4')
    version('2020.4', sha256='fc346005b3c19306ccf259329294d1d145a1294e04e9dbde2fb6c37697bb3917')
    version('2020.3', sha256='3513f7eb3f61817b6894b90832aa5eba513293f487d174ebc98f1bafc9165c64')
    version('2020.2', sha256='d29cdb53ee68abd5027eae07d9fd645b3f154e0d577efa2666c1334bb6d60efd')
    version('2020.1', sha256='a3e21cbac5f7103925872d80d806d8677f034f8ae8bb6bf6296af81ab028c23b')
    version('2020.0', sha256='60efe9b148f66aa1b29110493244dc9f1f1d722e6d96969e4d4b2c0ab9278104')
    version('2019.5', sha256='ffe5857a33068ec174140c154610d76d833524d840a2fc2d1a15e16686213cad')
    version('2019.4', sha256='a3564eb9727335352dc0cfa2f2b29474c2c837384689ac5fcb387784a56e7685')
    version('2019.3', sha256='2bd93fa14925a8dc63a67e64266c8ccd2fa3ac44b10253d93e6f8a630350070c')
    version('2019.2', sha256='fb656208ff7d4cd8b1b422f60c9e6d8747302a347cbf6c199d7afa9b80f80ea3')

    depends_on('libnl')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('batctl', prefix.bin)
