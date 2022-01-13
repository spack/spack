##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from .neurodamus_model import NeurodamusModel, \
    version_from_model_core_deps


class NeurodamusNeocortex(NeurodamusModel):
    """Neurodamus with built-in neocortex model
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/models/neocortex"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/models/neocortex.git"

    # IMPORTANT: Register versions (only) here to make them stable
    # Final version name is combined e.g. "1.0-3.0.1"
    model_core_dep_v = (
        ('1.5', '3.3.3'),
        ('1.4', '3.3.2'),
        ('1.3', '3.2.0'),
        ('1.2', '3.1.0'),
        ('1.1', '3.0.2'),
    )
    version_from_model_core_deps(model_core_dep_v)

    # Legacy versions
    version('develop', branch='main', submodules=True, get_full_repo=True)
    version('1.0', tag='1.0', submodules=True, get_full_repo=True)
    version('0.3', tag='0.3-1', submodules=True, get_full_repo=True)
    version('0.2', tag='0.2', submodules=True, get_full_repo=True)
    version('0.1', tag='0.1', submodules=True, get_full_repo=True)

    variant('v5', default=True, description='Enable support for previous v5 circuits')
    variant('plasticity', default=False, description="Use optimized ProbAMPANMDA_EMS and ProbGABAAB_EMS")

    mech_name = "neocortex"

    @run_before('build_model')
    def prepare_mods(self):
        if self.spec.satisfies('+v5'):
            copy_all('mod/v5', 'mod', make_link)
        copy_all('mod/v6', 'mod', make_link)
        # Plasticity
        if self.spec.satisfies('+plasticity'):
            copy_all('mod/v6/optimized', 'mod', make_link)
