# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RPbdzmq(RPackage):
    """'ZeroMQ' is a well-known library for high-performance asynchronous
    messaging in scalable, distributed applications. This package provides
    high level R wrapper functions to easily utilize 'ZeroMQ'. We mainly focus
    on interactive client/server programming frameworks. For convenience, a
    minimal 'ZeroMQ' library (4.1.0 rc1) is shipped with 'pbdZMQ', which can
    be used if no system installation of 'ZeroMQ' is available. A few wrapper
    functions compatible with 'rzmq' are also provided."""

    homepage = "http://r-pbd.org/"
    url      = "https://cran.r-project.org/src/contrib/pbdZMQ_0.2-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pbdZMQ"

    version('0.2-4', 'e5afb70199aa54d737ee7a0e26bde060')

    depends_on('r-r6', type=('build', 'run'))
    depends_on('zeromq')
