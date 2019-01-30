# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRzmq(RPackage):
    """Interface to the ZeroMQ lightweight messaging kernel."""

    homepage = "http://github.com/armstrtw/rzmq"
    url      = "https://cran.r-project.org/src/contrib/rzmq_0.7.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rzmq"

    version('0.7.7', '8ba18fd1c222d1eb25bb622ccd2897e0')

    depends_on('zeromq')
