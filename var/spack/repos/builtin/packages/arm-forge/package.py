# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import subprocess

from spack.package import *


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
        version("22.0.1", sha256="89237d85cdecf6481c1aa72f3a7c60145ff2f1efcf588aa382b98ee8046d1bd5")
        version("22.0",   sha256="30328b3f92d3284c632c196690a36bce8f3c83b17f2c810deb31797a9ac69432")
        version("21.1.3", sha256="4a4ff7372aad5a31fc9e18b7b6c493691ab37d8d44a3158584e62d1ab82b0eeb")
        version("21.1.2", sha256="9d62bb0b9411663693a4431c993a5a81ce84fc7d58c08d32c77e87fac7c44eb0")
        version("21.1.1", sha256="9215180dc42565c2ac45db8851d3ee5fcfe11f06ccbf655c2e800f32a3479f5d")
        version("21.1",   sha256="d6f6444eb2d47fd884d8b125f890d6a02a9d5bcfc10950af46b11d3b1e1189fd")
        version("21.0.3", sha256="371f4e3087af329bee155ceb50b9adaf006d3b8602fb1b6bbdc710ab0f74368d")
        version("21.0.2", sha256="ca547d11086ddd2704468166ad01f34132fcfa8d416239ad85c87a6c5f042298")
        version("21.0.1", sha256="bb76207b47079db843f189f604cffd00cffa49963c3e515092b67392047b92d2")
        version("21.0",   sha256="2bcc745d0049d6b25c77c97b2d7bad7b4f804180972a2306a8599ce41f6a4573")
    elif platform.machine() == "ppc64le":
        version("22.0.1", sha256="7499462f2f24a556b504c10e56cce61d8e29630ac99aa7a9a59f60e7ce474877")
        version("22.0",   sha256="dbe1248ba683b2b1374c888805c608252daade47f904fb91a4a4803bf11ea5fa")
        version("21.1.3", sha256="eecbc5686d60994c5468b2d7cd37bebe5d9ac0ba37bd1f98fbfc69b071db541e")
        version("21.1.2", sha256="3c1006e3a3ee0c3a1e73f984da19d9953fa48f31c89f8774954c885a070a76d8")
        version("21.1.1", sha256="305ee145040db30b7c7af6a05364030fe753c40cbf5cf3b4ea04a8812c2c3b49")
        version("21.1",   sha256="24e6fb120fcecf854a069ce6c993d430e892a18f415603009768e43317980491")
        version("21.0.3", sha256="a1dad6efdfa6bf95e5ec02f771217bf98d7d010c6bfdd5caf0796f0e75ef0fab")
        version("21.0.2", sha256="302cadf6c6ddd6f41fafb0d490a92ae0919a7b24d6c212228311253cec2ff1b7")
        version("21.0.1", sha256="fa9c1fbb115d34533f4dc449cb49c7eca0472205973ed1e9ab5ccd916c85a6f9")
        version("21.0",   sha256="60cfa7dd1cd131ec85e67cb660f2f84cf30bb700d8979cae1f5f88af658fd249")
    elif platform.machine() == "x86_64":
        version("22.0.1", sha256="8f8a61c159665d3de3bc5334ed97bdb4966bfbdb91b65d32d162d489eb2219ac")
        version("22.0",   sha256="4e63758bd474e9640700673625eb2adfe2bdf875eaacfe67862d184ae08f542f")
        version("21.1.3", sha256="03dc82f1d075deb6f08d1e3e6592dc9b630d406c08a1316d89c436b5874f3407")
        version("21.1.2", sha256="ebc99fa3461d2cd968e4d304c11b70cc8d9c5a2acd68681cec2067c128255cd5")
        version("21.1.1", sha256="b1f4a6cffca069b10bcee66ace38bd1a515f48fbae3c44ff6faef6825a633df5")
        version("21.1",   sha256="933dce5980ab0f977a79d24eecf4464bd7c5ff22fa74fb2758f68d1ccb7723d2")
        version("21.0.3", sha256="24708b363a8d3a82879ab4f60fe08faeb936e1e8286b324928a86a2d707071e8")
        version("21.0.2", sha256="741ff2a995c8cf7ce5d346a3f7d2a552ec602b995e477e9a5a3a6319d3907980")
        version("21.0.1", sha256="849c1443af3315b0b4dc2d8b337200cd92351cb11448bd3364428d8b6325ae5a")
        version("21.0",   sha256="71b713a05d431a3c26bd83cc4d0b65a0afd7d7f5bf57aa11edfb41da90f01774")

    variant('probe', default=False, description='Detect available PMU counters via "forge-probe" during install')

    # forge-probe executes with "/usr/bin/env python"
    depends_on('python@2.7:', type='build', when='+probe')

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
        return "https://content.allinea.com/downloads/arm-forge-%s-linux-%s.tar" % (version, platform.machine())

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
