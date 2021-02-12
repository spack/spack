# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Hudi(MavenPackage):
    """Apache Hudi stands for Hadoop Upserts Deletes and Incrementals.
    Hudi manages the storage of large analytical datasets on DFS."""

    homepage = "https://hudi.apache.org/"
    url      = "https://github.com/apache/hudi/archive/release-0.5.3.tar.gz"

    version('0.7.0', sha256='2130966b44a4c43a58f95bfa85e1e63c12c3b8f66ed5947acc46cc11cf322f54')
    version('0.6.0', sha256='fb38bc53a317e40525b9d4cdb5643598dbbccf46ec6da23552f0a510571b287a')
    version('0.5.3', sha256='8cbf52007fddd07eebd20c8962cd630b05a8ae4c597523fd63db837a45a0b227')

    depends_on('java@8', type=('build', 'run'))
