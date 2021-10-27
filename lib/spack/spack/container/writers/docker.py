# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.tengine as tengine

from . import PathContext, writer


@writer('docker')
class DockerContext(PathContext):
    """Context used to instantiate a Dockerfile"""
    #: Name of the template used for Dockerfiles
    template_name = 'container/Dockerfile'

    @tengine.context_property
    def manifest(self):
        manifest_str = super(DockerContext, self).manifest
        # Docker doesn't support HEREDOC so we need to resort to
        # a horrible echo trick to have the manifest in the Dockerfile
        echoed_lines = []
        for idx, line in enumerate(manifest_str.split('\n')):
            if idx == 0:
                echoed_lines.append('&&  (echo "' + line + '" \\')
                continue
            echoed_lines.append('&&   echo "' + line + '" \\')

        echoed_lines[-1] = echoed_lines[-1].replace(' \\', ')')

        return '\n'.join(echoed_lines)
