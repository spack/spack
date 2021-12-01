##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
from spack.pkg.builtin.neurodamus_model import NeurodamusModel, \
    version_from_model_core_deps


class NeurodamusHippocampus(NeurodamusModel):
    """Neurodamus with built-in Hippocampus model.
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/models/hippocampus"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/models/hippocampus.git"

    mech_name = "hippocampus"

    # IMPORTANT: Register versions (only) here to make them stable
    # Final version name is combined e.g. "1.0-3.0.1"
    model_core_dep_v = (
        ('1.5', '3.3.3'),
        ('1.4.1', '3.2.0'),
        ('1.3', '3.1.0'),
        ('1.2', '3.1.0'),
        ('1.1', '3.0.2'),
    )
    version_from_model_core_deps(model_core_dep_v)

    # Legacy versions
    version('develop', branch='main', submodules=True, get_full_repo=False)
    version('1.0', tag='1.0', submodules=True, get_full_repo=False)
    version('0.4', tag='0.4-1', submodules=True, get_full_repo=False)
    version('0.3', tag='0.3', submodules=True, get_full_repo=False)
    version('0.2', tag='0.2', submodules=True, get_full_repo=False)
    version('0.1', tag='0.1', submodules=True, get_full_repo=False)
