# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusNeocortex(NeurodamusModel):
    """Neurodamus with built-in neocortex model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/neocortex"
    git      = "ssh://bbpcode.epfl.ch/sim/models/neocortex"

    version('develop', git=git, branch='master', submodules=True, clean=False)
    version('0.1', git=git, tag='0.1', submodules=True, clean=False)

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
