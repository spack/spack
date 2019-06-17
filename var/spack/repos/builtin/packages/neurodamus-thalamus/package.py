# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusThalamus(NeurodamusModel):
    """Neurodamus with built-in Thalamus model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/thalamus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/thalamus"

    version('develop', git=git, branch='master', submodules=True, clean=False)
    version('0.1', git=git, tag='0.1', submodules=True, clean=False)
