# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NcbiBlast(AutotoolsPackage):
    """Basic Local Alignment Search Tool"""

    homepage = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
    url      = "https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.10.0/ncbi-blast-2.10.0+-src.tar.gz"
    list_url = url
    list_depth = 1

    version('2.10.0', sha256='3acdd9cec01c4f43e56aeaf89049cb8f8013d60b9c1705eced10166967f1d926')
    version('2.9.0', sha256='a390cc2d7a09422759fc178db84de9def822cbe485916bbb2ec0d215dacdc257')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    configure_directory = 'c++'
    build_directory = 'c++'
