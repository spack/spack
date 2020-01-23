# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusHippocampus(NeurodamusModel):
    """Neurodamus with built-in Hippocampus model.
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"

    mech_name = "hippocampus"

    version('develop', branch='master', submodules=True, get_full_repo=False)
    version('0.4', tag='0.4-1', submodules=True, get_full_repo=False)
    version('0.3', tag='0.3', submodules=True, get_full_repo=False)
    version('0.2', tag='0.2', submodules=True, get_full_repo=False)
    version('0.1', tag='0.1', submodules=True, get_full_repo=False)
