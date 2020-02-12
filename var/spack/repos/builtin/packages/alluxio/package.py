# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alluxio(Package):
    """
    Alluxio (formerly known as Tachyon) is a virtual distributed storage
    system. It bridges the gap between computation frameworks and storage
    systems, enabling computation applications to connect to numerous
    storage systems through a common interface.
    """

    homepage = "https://github.com/Alluxio/alluxio"
    url      = "https://github.com/Alluxio/alluxio/archive/v2.1.0.tar.gz"

    version('2.1.0', sha256='c8b5b7848488e0ac10b093eea02ef05fa822250669d184291cc51b2f8aac253e')

    def install(self, spec, prefix):
        install_tree('.', prefix)
