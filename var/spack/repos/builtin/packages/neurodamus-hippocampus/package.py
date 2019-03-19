# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusHippocampus(NeurodamusModel):
    """Neurodamus with built-in Hippocampus model.
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"

    version('develop', git=git, branch='master', submodules=True)
    version('0.2', git=git, tag='0.2', submodules=True, preferred=True)
    version('0.1', git=git, tag='0.1', submodules=True)
