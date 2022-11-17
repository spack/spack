##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from .neurodamus_model import (
    NeurodamusModel,
    copy_all,
    make_link,
    version_from_model_core_dep,
    version_from_model_ndpy_dep,
)


class NeurodamusNeocortex(NeurodamusModel):
    """Neurodamus with built-in neocortex model
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/models/neocortex"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/sim/models/neocortex.git"

    variant('v5',         default=True, description='Enable support for previous v5 circuits')
    variant('plasticity', default=False, description="Use optimized ProbAMPANMDA_EMS and ProbGABAAB_EMS")
    variant('ngv',        default=False, description="Include NGV mod files")
    variant('metabolism', default=False, description="Use metabolism related mod files")

    conflicts("+coreneuron", when="+ngv")
    conflicts("+coreneuron", when="+metabolism")

    mech_name = "neocortex"

    version('develop', branch='main', submodules=True, get_full_repo=True)

    # IMPORTANT: Register new versions only using version_from_model_*
    # Final version name is combined e.g. "1.0-3.0.1"
    version_from_model_ndpy_dep('1.9')
    version_from_model_ndpy_dep('1.8')
    version_from_model_ndpy_dep('1.7')
    version_from_model_ndpy_dep('1.6')
    version_from_model_core_dep('1.5', '3.3.4')

    @run_before('build_model')
    def prepare_mods(self):
        if self.spec.satisfies('+v5'):
            copy_all('mod/v5', 'mod', make_link)
        copy_all('mod/v6', 'mod', make_link)

        # Plasticity
        if self.spec.satisfies('+plasticity'):
            copy_all('mod/v6/optimized', 'mod', make_link)

        # NGV must overwrite other mods, even from the specific
        # models, e.g. ProbAMPANMDA
        if self.spec.satisfies("+ngv"):
            copy_all('common_latest/common/mod/ngv', 'mod', make_link)

        # Metabolism takes precedence over all mod files
        if self.spec.satisfies('+metabolism'):
            copy_all('mod/metabolism', 'mod', make_link)
