# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PmgrCollective(Package):
    """PMGR_COLLECTIVE provides a scalable network for bootstrapping
       MPI jobs."""
    homepage = "http://www.sourceforge.net/projects/pmgrcollective"
    url      = "http://downloads.sourceforge.net/project/pmgrcollective/pmgrcollective/PMGR_COLLECTIVE-1.0/pmgr_collective-1.0.tgz"

    version('1.0', '0384d008774274cc3fc7b4d810dfd07e')

    def install(self, spec, prefix):
        make('PREFIX="' + prefix + '"')
        make('PREFIX="' + prefix + '"', "install")
