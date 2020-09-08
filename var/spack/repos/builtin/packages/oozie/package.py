# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Oozie(MavenPackage):
    """Oozie is an extensible, scalable and reliable system to define,
    manage, schedule, and execute complex Hadoop workloads via web services."""

    homepage = "https://oozie.apache.org/"
    url      = "https://github.com/apache/oozie/archive/release-5.2.0.tar.gz"

    version('5.2.0', sha256='998741fb64b0badef917586685f8da90c5f037da9ed187361ac8db888780bf14')

    depends_on('java@8', type=('build', 'run'))
