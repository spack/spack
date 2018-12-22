# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dmtcp(AutotoolsPackage):
    """DMTCP (Distributed MultiThreaded Checkpointing) transparently
    checkpoints a single-host or distributed computation in user-space --
    with no modifications to user code or to the O/S."""

    homepage = "http://dmtcp.sourceforge.net/"
    url      = "https://sourceforge.net/projects/dmtcp/files/2.5.2/dmtcp-2.5.2.tar.gz/download"

    version('2.5.2', sha256='0e3e5e15bd401b7b6937f2b678cd7d6a252eab0a143d5740b89cc3bebb4282be')
