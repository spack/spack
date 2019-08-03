# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RProto(RPackage):
    """An object oriented system using object-based, also called
    prototype-based, rather than class-based object oriented ideas."""

    homepage = "http://r-proto.googlecode.com/"
    url      = "https://cloud.r-project.org/src/contrib/proto_0.3-10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/proto"

    version('1.0.0', sha256='9294d9a3b2b680bb6fac17000bfc97453d77c87ef68cfd609b4c4eb6d11d04d1')
    version('0.3-10', 'd5523943a5be6ca2f0ab557c900f8212')
