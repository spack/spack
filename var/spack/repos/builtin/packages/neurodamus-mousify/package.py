# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusMousify(NeurodamusModel):
    """Neurodamus with built-in Mousify model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/mousify"
    git      = "ssh://bbpcode.epfl.ch/sim/models/mousify"

    mech_name = "mousify"

    version('develop', branch='master', submodules=True, get_full_repo=False)
    version('0.3', git=git, tag='0.3-1', submodules=True, get_full_repo=False)
    version('0.2', git=git, tag='0.2', submodules=True, get_full_repo=False)
    version('0.1', git=git, tag='0.1', submodules=True, get_full_repo=False)
