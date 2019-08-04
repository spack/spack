# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRzmq(RPackage):
    """Interface to the ZeroMQ lightweight messaging kernel."""

    homepage = "http://github.com/armstrtw/rzmq"
    url      = "https://cloud.r-project.org/src/contrib/rzmq_0.7.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rzmq"

    version('0.9.6', sha256='80a3fc6eb6f7851224c4cd5e219ca4db0286551ad429359d4df853ccb9234316')
    version('0.9.4', sha256='03fbda756d823c11fba359b94a6213c3440e61973331668eaac35779717f73ad')
    version('0.7.7', '8ba18fd1c222d1eb25bb622ccd2897e0')

    depends_on('zeromq')
