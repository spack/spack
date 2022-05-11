# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import subprocess

from spack.package_defs import *


class ArmForge(Package):
    """Arm Forge is the complete toolsuite for software development - with
    everything needed to debug, profile, optimize, edit and build C, C++ and
    Fortran applications on Linux for high performance - from single threads
    through to complex parallel HPC codes with MPI, OpenMP, threads or CUDA."""

    homepage = "https://www.arm.com/products/development-tools/server-and-hpc/forge"
    maintainers = ["NickRF"]

    # TODO: this mess should be fixed as soon as a way to parametrize/constrain
    #       versions (and checksums) based on the target platform shows up

    if platform.machine() == "aarch64":
        version("21.1",   sha256="d6f6444eb2d47fd884d8b125f890d6a02a9d5bcfc10950af46b11d3b1e1189fd")
        version("21.0.2", sha256="ca547d11086ddd2704468166ad01f34132fcfa8d416239ad85c87a6c5f042298")
        version("21.0",   sha256="2bcc745d0049d6b25c77c97b2d7bad7b4f804180972a2306a8599ce41f6a4573")
    elif platform.machine() == "ppc64le":
        version("21.1",   sha256="24e6fb120fcecf854a069ce6c993d430e892a18f415603009768e43317980491")
        version("21.0.2", sha256="302cadf6c6ddd6f41fafb0d490a92ae0919a7b24d6c212228311253cec2ff1b7")
        version("21.0",   sha256="60cfa7dd1cd131ec85e67cb660f2f84cf30bb700d8979cae1f5f88af658fd249")
    elif platform.machine() == "x86_64":
        version("21.1",   sha256="933dce5980ab0f977a79d24eecf4464bd7c5ff22fa74fb2758f68d1ccb7723d2")
        version("21.0.2", sha256="741ff2a995c8cf7ce5d346a3f7d2a552ec602b995e477e9a5a3a6319d3907980")
        version("21.0",   sha256="71b713a05d431a3c26bd83cc4d0b65a0afd7d7f5bf57aa11edfb41da90f01774")

    variant('probe', default=False, description='Detect available PMU counters via "forge-probe" during install')

    # forge-probe executes with "/usr/bin/env python"
    depends_on('python@2.7:2.9.9', type='build', when='+probe')

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licences/Licence"]
    license_vars = [
        "ALLINEA_LICENSE_DIR",
        "ALLINEA_LICENCE_DIR",
        "ALLINEA_LICENSE_FILE",
        "ALLINEA_LICENCE_FILE",
    ]
    license_url = "https://developer.arm.com/tools-and-software/server-and-hpc/help/help-and-tutorials/system-administration/licensing/arm-licence-server"

    def url_for_version(self, version):
        return "http://content.allinea.com/downloads/arm-forge-%s-linux-%s.tar" % (version, platform.machine())

    def install(self, spec, prefix):
        subprocess.call(["./textinstall.sh", "--accept-licence", prefix])
        if spec.satisfies('+probe'):
            probe = join_path(prefix, "bin", "forge-probe")
            subprocess.call([probe, "--install", "global"])

    def setup_run_environment(self, env):
        # Only PATH is needed for Forge.
        # Adding lib to LD_LIBRARY_PATH can cause conflicts with Forge's internal libs.
        env.clear()
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
