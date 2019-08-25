# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRjava(RPackage):
    """Low-level interface to Java VM very much like .C/.Call and friends.
    Allows creation of objects, calling methods and accessing fields."""

    homepage = "http://www.rforge.net/rJava/"
    url      = "https://cloud.r-project.org/src/contrib/rJava_0.9-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rJava"

    version('0.9-11', sha256='c28ae131456a98f4d3498aa8f6eac9d4df48727008dacff1aa561fc883972c69')
    version('0.9-8', '51ae0d690ceed056ebe7c4be71fc6c7a')

    depends_on('r@2.5:', type=('build', 'run'))
    depends_on('java@1.2:')
    depends_on('gmake', type='build')
