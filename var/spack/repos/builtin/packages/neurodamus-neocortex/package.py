# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel
import shutil


class NeurodamusNeocortex(NeurodamusModel):
    """Neurodamus with built-in neocortex model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/neocortex"
    git      = "ssh://bbpcode.epfl.ch/sim/models/neocortex"

    version('develop', git=git, branch='master', submodules=True)
    version('1.1', tag='1.1', submodules=True)

    variant('v5', default=True, description='Enable support for previous v5 circuits')

    @run_before('merge_hoc_mod')
    def include_v5(self):
        if self.spec.satisfies('+v5'):
            self.copy_all('mod/v5', 'mod', copyfunc=shutil.move)

