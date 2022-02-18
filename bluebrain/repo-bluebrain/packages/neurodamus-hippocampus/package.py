##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *

from .neurodamus_model import (
    NeurodamusModel,
    version_from_model_core_dep,
    version_from_model_ndpy_dep,
)


class NeurodamusHippocampus(NeurodamusModel):
    """Neurodamus with built-in Hippocampus model.
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/models/hippocampus"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/models/hippocampus.git"

    mech_name = "hippocampus"

    version('develop', branch='main', submodules=True, get_full_repo=True)
    # IMPORTANT: Register new versions only using version_from_model_*
    # Final version name is combined e.g. "1.0-3.0.1"
    version_from_model_ndpy_dep('1.6')
    version_from_model_core_dep('1.5', '3.3.4')
