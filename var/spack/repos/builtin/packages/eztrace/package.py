# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eztrace(AutotoolsPackage):
    """EZTrace is a tool to automatically generate execution traces
       of HPC applications."""

    homepage = "http://eztrace.gforge.inria.fr"
    url      = "https://gforge.inria.fr/frs/download.php/file/37703/eztrace-1.1-8.tar.gz"

    version('1.1-8', sha256='d80d78a25f1eb0e6e60a3e535e3972cd178c6a8663a3d6109105dfa6a880b8ec')

    depends_on('mpi')

    # Does not work on Darwin due to MAP_POPULATE
    conflicts('platform=darwin')

    def configure_args(self):
        args = ["--with-mpi={0}".format(self.spec["mpi"].prefix)]
        return args
