# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from . import writer, PathContext


@writer('singularity')
class SingularityContext(PathContext):
    """Context used to instantiate a Singularity definition file"""
    #: Name of the template used for Singularity definition files
    template_name = 'container/singularity.def'
