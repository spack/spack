# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

    Note: Orca is licensed software. You will need to create an account
    on the Orca homepage and download Orca yourself. Spack will search
    your current directory for the download file. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://cec.mpg.de"
    url = "file://{0}/orca_4_0_1_2_linux_x86-64_openmpi202.tar.zst".format(os.getcwd())
    maintainers("snehring")
    manual_download = True

    version(
        "5.0.3-f.1",
        sha256="dea377459d61ef7d7e822e366420197ee2a4864991dfcdc4ea1a683f9be26c7f",
        url="file://{0}/orca-5.0.3-f.1_linux_x86-64_shared_openmpi41.tar.xz".format(os.getcwd()),
    )
    version(
        "5.0.3",
        sha256="b8b9076d1711150a6d6cb3eb30b18e2782fa847c5a86d8404b9339faef105043",
        url="file://{0}/orca_5_0_3_linux_x86-64_shared_openmpi411.tar.xz".format(os.getcwd()),
    )
    version(
        "4.2.1",
        sha256="9bbb3bfdca8220b417ee898b27b2885508d8c82799adfa63dde9e72eab49a6b2",
        expand=False,
    )
    version(
        "4.2.0",
        sha256="55a5ca5aaad03396ac5ada2f14b61ffa735fdc2d98355e272465e07a6749d399",
        expand=False,
    )
    version(
        "4.0.1.2",
        sha256="cea442aa99ec0d7ffde65014932196b62343f7a6191b4bfc438bfb38c03942f7",
        expand=False,
    )

    depends_on("zstd", when="@:4.2.1", type="build")
    depends_on("libevent", type="run")
    depends_on("libpciaccess", type="run")

    # Map Orca version with the required OpenMPI version
    openmpi_versions = {
        "4.0.1.2": "2.0.2",
        "4.2.0": "3.1.4",
        "4.2.1": "3.1.4",
        "5.0.3": "4.1.2",
        "5.0.3-f.1": "4.1.2",
    }
    for orca_version, openmpi_version in openmpi_versions.items():
        depends_on(
            "openmpi@{0}".format(openmpi_version), type="run", when="@{0}".format(orca_version)
        )

    def url_for_version(self, version):
        out = "file://{0}/orca_{1}_linux_x86-64_openmpi{2}.tar.zst"
        return out.format(os.getcwd(), version.underscored, self.openmpi_versions[version.string])

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        if self.spec.satisfies("@:4.2.1"):
            vername = os.path.basename(self.stage.archive_file).split(".")[0]

            zstd = which("zstd")
            zstd("-d", self.stage.archive_file, "-o", vername + ".tar")

            tar = which("tar")
            tar("-xvf", vername + ".tar")

            # there are READMEs in there but they don't hurt anyone
            install_tree(vername, prefix.bin)
        if self.spec.satisfies("@5.0.3-f.1"):
            install_tree("bin", prefix.bin)
            install_tree("lib", prefix.lib)
        else:
            install_tree(".", prefix.bin)

        # Check "mpirun" usability when building against OpenMPI
        # with Slurm scheduler and add a "mpirun" wrapper that
        # calls "srun" if need be
        if "^openmpi ~legacylaunchers schedulers=slurm" in self.spec:
            mpirun_srun = join_path(os.path.dirname(__file__), "mpirun_srun.sh")
            install(mpirun_srun, prefix.bin.mpirun)

    def setup_run_environment(self, env):
        # In 5.0.3-f.1 an RPATH is set to $ORGIN/../lib
        if not self.spec.satisfies("@5.0.3-f.1"):
            env.prepend_path("LD_LIBRARY_PATH", self.prefix.bin)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libevent"].prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libpciaccess"].prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["openmpi"].prefix.lib)
