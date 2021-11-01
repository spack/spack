# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.tengine as tengine

from . import PathContext, writer


@writer('singularity')
class SingularityContext(PathContext):
    """Context used to instantiate a Singularity definition file"""
    #: Name of the template used for Singularity definition files
    template_name = 'container/singularity.def'

    @property
    def singularity_config(self):
        return self.container_config.get('singularity', {})

    @tengine.context_property
    def runscript(self):
        return self.singularity_config.get('runscript', '')

    @tengine.context_property
    def startscript(self):
        return self.singularity_config.get('startscript', '')

    @tengine.context_property
    def test(self):
        return self.singularity_config.get('test', '')

    @tengine.context_property
    def help(self):
        return self.singularity_config.get('help', '')
