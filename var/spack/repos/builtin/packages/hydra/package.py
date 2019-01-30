# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hydra(AutotoolsPackage):
    """Hydra is a process management system for starting parallel jobs.
    Hydra is designed to natively work with existing launcher daemons
    (such as ssh, rsh, fork), as well as natively integrate with resource
    management systems (such as slurm, pbs, sge)."""

    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.2/hydra-3.2.tar.gz"
    list_url = "http://www.mpich.org/static/downloads/"
    list_depth = 1

    version('3.2', '4d670916695bf7e3a869cc336a881b39')
