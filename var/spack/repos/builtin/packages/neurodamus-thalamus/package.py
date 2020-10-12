# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel


class NeurodamusThalamus(NeurodamusModel):
    """Neurodamus with built-in Thalamus model
    """

    homepage = "ssh://bbpcode.epfl.ch/sim/models/thalamus"
    git      = "ssh://bbpcode.epfl.ch/sim/models/thalamus"

    mech_name = "thalamus"

    version('develop', branch='master', submodules=True, get_full_repo=False)
    version('1.0', tag='1.0', submodules=True, get_full_repo=False)
    version('0.3', tag='0.3-1', submodules=True, get_full_repo=False)
    version('0.2', tag='0.2', submodules=True, get_full_repo=False)
    version('0.1', tag='0.1', submodules=True, get_full_repo=False)
