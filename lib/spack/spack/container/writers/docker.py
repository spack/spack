# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import shlex

import spack.tengine as tengine

from . import PathContext, writer


@writer("docker")
class DockerContext(PathContext):
    """Context used to instantiate a Dockerfile"""

    #: Name of the template used for Dockerfiles
    template_name = "container/Dockerfile"

    @tengine.context_property
    def manifest(self):
        manifest_str = super().manifest
        # Docker doesn't support HEREDOC, so we need to resort to
        # a horrible echo trick to have the manifest in the Dockerfile
        echoed_lines = []
        for idx, line in enumerate(manifest_str.split("\n")):
            quoted_line = shlex.quote(line)
            if idx == 0:
                echoed_lines.append("&&  (echo " + quoted_line + " \\")
                continue
            echoed_lines.append("&&   echo " + quoted_line + " \\")

        echoed_lines[-1] = echoed_lines[-1].replace(" \\", ")")

        return "\n".join(echoed_lines)
