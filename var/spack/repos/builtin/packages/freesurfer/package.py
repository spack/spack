# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freesurfer(Package):
    """Freesurfer is an open source software suite for processing and analyzing
    (human) brain MRI images."""

    homepage = "https://freesurfer.net/"

    # A license is required, but is free to obtain.
    license_required = True
    license_files = ["./license.txt"]

    maintainers("robgics")

    version("7.2.0", sha256="4cca78602f898bf633428b9d82cbb9b07e3ab97a86c620122050803779c86d62")
    version("7.1.1", sha256="6098b166fee8644f44f9ec88f3ffe88d05f2bc033cca60443e99e3e56f2e166b")
    version("7.1.0", sha256="1b8f26fe5c712433ddb74c47fe1895ed1d9fbff46cfae8aaae2697cb65ae8840")

    depends_on("mesa-glu")
    depends_on("qt")

    def url_for_version(self, version):
        return "https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/{0}/freesurfer-linux-centos7_x86_64-{1}.tar.gz".format(
            version, version
        )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.set("FREESURFER_HOME", self.prefix)
        env.set("SUBJECTS_DIR", join_path(self.prefix, "subjects"))
        env.set("FUNCTIONALS_DIR", join_path(self.prefix, "sessions"))

    def install(self, spec, prefix):
        install_tree(".", prefix)
