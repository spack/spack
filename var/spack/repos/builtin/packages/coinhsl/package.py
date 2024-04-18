# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os

class Coinhsl(MesonPackage, AutotoolsPackage):
    """CoinHSL is a collection of linear algebra libraries (KB22, MA27,
    MA28, MA54, MA57, MA64, MA77, MA86, MA97, MC19, MC34, MC64, MC68,
    MC69, MC78, MC80, OF01, ZB01, ZB11) bundled for use with IPOPT and
    other applications that use these HSL routines.

    Note: CoinHSL is licensed software. You will need to request a
    license from Research Councils UK and download a .tar.gz archive
    of CoinHSL yourself. Spack will search your current directory for
    the download file. Alternatively, add this file to a mirror so
    that Spack can find it. For instructions on how to set up a
    mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    build_system(
        conditional("autotools", when="@b:2019.05.21"),
        conditional("meson", when="@2022.11.09:,:b"),
        default="meson",
    )

    homepage = "https://www.hsl.rl.ac.uk/ipopt/"
    url = f"file://{os.getcwd()}/coinhsl-2023.11.17.tar.gz"
    manual_download = True

    maintainers("AndrewLister-STFC")

    # Meson builds
    version(
        "2023.11.17",
        sha256="43438fb9317dd4648625a6f5dd46ffedf1d33bd47d05885805b651fe93729065",
        preferred=True,
    )
    version(
        "archive-2023.11.17",
        sha256="8bb19f6e4ed6057cea801b116f0b86868a100d378952c827092b9c9dbedfc4d2",
    )
    version(
        "2023.05.26", sha256="e39faf1edb5ce83ff80e443f6d7ebb322fa6abfc5286cb54d6a6030c4a826306"
    )
    version(
        "archive-2023.05.26",
        sha256="6fd92bbbb2eaa22de5bd9944a282e0089f6a90fb10dbc991182a67b07eaafce7",
    )
    version(
        "archive-2022.12.02",
        sha256="5ebdbf8a70a9e10863c5809cf53e4e236b07f65ab2e96cc367ba8131dc19e232",
    )
    version(
        "2022.11.09", sha256="d6d9089bb9cf3eb0e4af195f1a2f10cd61da42eddf8da73a12b8c62902bceee3"
    )

    with when("build_system=meson @2022:"):
        depends_on("blas")
        depends_on("lapack")
        variant("metis", default=True, description="Build with Metis support.")
        depends_on("metis", when="+metis")

    def meson_args(self):
        spec = self.spec
        args = []
        if spec.satisfies("@2022:"):
            return []

        blas = spec["blas"].names[0]
        blas_paths = [sf[2:] for sf in spec["blas"].search_flags.split()]
        lapack = spec["lapack"].names[0]
        lapack_paths = [sf[2:] for sf in spec["lapack"].search_flags.split()]
        args.append(f"-Dlibblas={blas}")
        args.extend([f"-Dlibblas_path={p}" for p in blas_paths])
        args.append(f"-Dliblapack={lapack}")
        args.extend([f"-Dlibblas_path={p}" for p in lapack_paths])
        if spec.satisfies("+metis"):
            metis = spec["metis"]
            if metis.satisfies("@5"):
                args.append("-Dlibmetis_version=5")
            else:
                args.append("-Dlibmetis_version=4")
            args.extend(
                [
                    f"-Dlibmetis_include={metis.prefix.include}",
                    f"-Dlibmetis_path={metis.prefix.lib}",
                ]
            )

    # Autotools builds
    version(
        "2019.05.21", sha256="95ce1160f0b013151a3e25d40337775c760a8f3a79d801a1d190598bf4e4c0c3"
    )
    version(
        "2015.06.23", sha256="3e955a2072f669b8f357ae746531b37aea921552e415dc219a5dd13577575fb3"
    )
    version(
        "2014.01.17", sha256="ed49fea62692c5d2f928d4007988930da9ff9a2e944e4c559d028671d122437b"
    )
    version(
        "2014.01.10", sha256="7c2be60a3913b406904c66ee83acdbd0709f229b652c4e39ee5d0876f6b2e907"
    )

    with when("build_system=autotools"):
        parallel = False
        variant("blas", default=False, description="Link to external BLAS library")
        depends_on("blas", when="+blas")

    def configure_args(self):
        spec = self.spec
        args = []
        if spec.satisfies("+blas"):
            args.append(f"--with-blas={spec['blas'].libs.ld_flags}")
        return args
