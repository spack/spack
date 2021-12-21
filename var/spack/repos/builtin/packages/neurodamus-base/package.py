##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os
import shutil


class NeurodamusBase(Package):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/archive/neurodamus-bbp"
    url      = "git@bbpgitlab.epfl.ch:hpc/archive/neurodamus-bbp.git"

    version('master',      git=url, branch='master')
    version('mousify',     git=url, branch='sandbox/leite/mousify')
    version('hippocampus', git=url, branch='sandbox/king/hippocampus')
    version('plasticity',  git=url, branch='sandbox/king/saveupdate_v6support_mask', preferred=True)

    def install(self, spec, prefix):
        shutil.copytree('lib', prefix.lib)
        if os.path.isdir('python'):
            shutil.copytree('python', prefix.python)
