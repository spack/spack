# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nvidia-nsight-systems
#
# You can edit this file again by typing:
#
#     spack edit nvidia-nsight-systems
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
from glob import glob
import shutil
import os


class NvidiaNsightSystems(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "nvidia-nsight-systems"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("scothalverson")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

    # FIXME: Add proper versions here.
    # version("1.2.4")

    # FIXME: Add dependencies if required.
    depends_on("libarchive programs='bsdtar'")

    
    version('2024.1.1', sha256='b67168897c30b8f7a2c5c2ff1b2bc2bf1a544d4a220bf6eb0db6af9835aefe07', url='https://developer.download.nvidia.com/devtools/repos/rhel8/arm64/nsight-systems-cli-2024.1.1-2024.1.1.59_3380207-0.aarch64.rpm', expand=False)

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        bsdtar = which("bsdtar")
        rpm_file = glob(join_path(self.stage.source_path, "nsight-systems*.rpm"))[0]
        

        params = ['-x', '-f', rpm_file]

        ver = prefix.split("/")[-1].split("-")[-2]
        bsdtar(*params)
        params = ['-x', '-f', 'data.tar.gz']
        bsdtar(*params)
        for sd in ["/documentation", "/host-linux-armv8", "/target-linux-sbsa-armv8"]:
            shutil.copytree("opt/nvidia/nsight-systems/"+ver + sd, prefix + sd)
        os.mkdir(prefix + "/bin")
        os.symlink(prefix + "/host-linux-armv8/nsys-ui", prefix + "/bin/nsys-ui")
        os.symlink(prefix + "/target-linux-sbsa-armv8/nsys", prefix + "/bin/nsys")

        
