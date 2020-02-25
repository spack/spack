# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Optix(Package):
    """Nvidia OptiX is a ray tracing API."""

    homepage = "https://developer.nvidia.com/optix"
    version(
        "5.0.1",
        sha256="2f03dcdd15550fb54db4ad0b0c4741c85b2964d59bf39895ebda74f91fef3c55",
        extension="sh",
        expand=False,
    )
    url = "file:///gpfs/bbp.cscs.ch/project/proj3/development/deployment/optix.sh"
    phases = ["install"]

    def install(self, spec, prefix):
        set_executable("./optix.sh")
        install = Executable("./optix.sh")
        install("--skip-license", "--prefix=%s" % prefix)
