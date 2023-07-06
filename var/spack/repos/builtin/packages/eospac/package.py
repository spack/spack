# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Eospac(Package):
    """A collection of C routines that can be used to access the Sesame data
    library.
    """

    homepage = "https://laws.lanl.gov/projects/data/eos.html"
    list_url = "https://laws.lanl.gov/projects/data/eos/eospacReleases.php"
    maintainers("KineticTheory")

    # - An EOSPAC release labeled "beta" doesn't always imply that the release
    #   is less suitable for production.  According to the current EOSPAC
    #   release procedure, even a release that only fixes known bugs in a
    #   previous stable release will appear first as a new beta.
    # - alpha and beta versions are marked with 'deprecated=True' to help
    #   spack's version comparison.
    version(
        "6.5.6",
        preferred=True,
        sha256="49bae52a0c1dc249ca75d47fc1ff9d6367221aa5a5a9c4664efaea6f0292eaff",
        url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.5.6_a523d0d98e0323fc0e3aa1c6ad540ebc741c3982.tgz",
    )
    version(
        "6.5.5",
        sha256="2b8129e02dce0d87f0006c82a0849172c3bc13c346485c54e6400a522f8fd754",
        url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.5.5_dcc5ca928b63c0add278107bef33a6bdd8befe44.tgz",
    )
    version(
        "6.5.0",
        sha256="4e539418f773a5bd00dc49a5000ca857e5228cc5e83f198d46827a5671d34cff",
        url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.5.0_6b10f4ccc1fc333b5d6023b93ab194ab0621d5ae.tgz",
    )
    version(
        "6.5.0beta",
        sha256="42e6d491aaf296e4d6ab946481aaafd64b0a4e9801fc2ff098cc16aa118f54c8",
        url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.5.0beta_859ce5b1b8c4106057ca61d03a6c9c713a7f0328.tgz",
        deprecated=True,
    )
    version(
        "6.5.0alpha.1",
        sha256="c7334342dd2e071e17c60d8fabb11d2908c9d48c9b49ea83c3609a10b7b8877b",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.5.0alpha.1_62053188b9842842e41508c54196c533e0b91e51.tgz",
        deprecated=True,
    )
    version(
        "6.4.2",
        sha256="13627a5c94d3a456659d1bba0f3cec157380933fbd401e13e25906166150a252",
        url="https://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.2_e2f7906a0863932e3d65d329f789c4b90c6be58d.tgz",
    )
    version(
        "6.4.2beta",
        sha256="635b94f1ec7558deca92a3858c92db0f4437170252bb114cbdb809b74b6ee870",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.2beta_a62baf70708536f6fb5486e315c730fa76c1f6b5.tgz",
        deprecated=True,
    )
    version(
        "6.4.1",
        sha256="2310c49bd7a60cad41d2cb1059c5f0a1904f0c778b164937182382df326ca003",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.1_0cc1bc21a8bb1adadbae0dd3a2135790e8119320.tgz",
    )
    version(
        "6.4.1beta",
        sha256="479074a7be724760f8f1f90a8673f6197b7c5aa1ff76242ecf3790c9016e08c3",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.1beta_b651322c74cf5729732afd5d77c66c41d677be5e.tgz",
        deprecated=True,
    )
    version(
        "6.4.1alpha.2",
        sha256="cd075e7a41137da85ee0680c64534675d50979516e9639b17fa004619651ac47",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.1alpha.2_e2aaba283f57511b94afa9283e5ee794b03439dc.tgz",
        deprecated=True,
    )
    version(
        "6.4.0",
        sha256="15a953beac735c68431afe86ffe33323d540d0fbbbec03ba79438dd29736051d",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0_612ea8c9b8ffa6d9175d9118955571d9107f1e3c.tgz",
    )
    version(
        "6.4.0beta.4",
        sha256="0ebfd8badff575ea77444aa978629dbdca3135a0b5eb373b8daba058773d4635",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.4_aff6429bb6868de31a980278bafa13487c2ce83f.tgz",
        deprecated=True,
    )
    version(
        "6.4.0beta.3",
        sha256="9f387ca5356519494c6f3f27adb0c165cf9f9e15e3355a67bf940a4a92eebdab",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.3_90ff265f62aa1780bfcd0a62dad807b6be6ed461.tgz",
        deprecated=True,
    )
    version(
        "6.4.0beta.2",
        sha256="f9db46cd6c62a6f83960d802350f3e37675921af102969b293c02eb797558a53",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.2_69196eadbc77506561eef711f19d2f03b4ab0ffa.tgz",
        deprecated=True,
    )
    version(
        "6.4.0beta.1",
        sha256="14c5c804e5f628f41e8ed80bcee5a80adeb6c6f3d130715421ca99a30c7eb7e2",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.1_r20171213193219.tgz",
        deprecated=True,
    )
    version(
        "6.3.1",
        sha256="aa1112c4251c9c3c2883a7ab2c7f2abff2c339f29dbbf8421ef88b0c9df904f8",
        url="http://laws.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.3.1_r20161202150449.tgz",
    )

    # This patch allows the use of spack's compile wrapper 'flang'
    patch("flang.patch", when="@:6.4.0beta.2%clang")
    patch("frt.patch", when="%fj")
    # This patch corrects EOSPAC's selection of compiler flags when
    # compilers are specified using absolute pathnames.
    patch("cpuinfo_comp_flags_key.patch", when="@:6.4.1,6.4.2beta")
    # This patchset corrects EOSPAC's selection of compiler flags when
    # intel-classic@2021 is used.
    patch("650-ic2021.patch", when="@6.5.0%intel")
    patch("642-ic2021.patch", when="@6.4.2%intel")
    patch("641-ic2021.patch", when="@6.4.1%intel")
    patch("640-ic2021.patch", when="@6.4.0%intel")

    # GPU offload is only available for version 6.5+
    variant("offload", default=False, description="Build GPU offload library instead of standard")
    conflicts("+offload", when="@:6.4.99")

    def install(self, spec, prefix):
        with working_dir("Source"):
            compilerArgs = []
            compilerArgs.append("CC={0}".format(spack_cc))
            compilerArgs.append("CXX={0}".format(spack_cxx))
            compilerArgs.append("F77={0}".format(spack_f77))
            compilerArgs.append("F90={0}".format(spack_fc))
            # This looks goofy because eospac does not actually respect the
            # value of DO_OFFLOAD and instead only attempts to check for its
            # existence; a quirk of eospac.
            if "+offload" in spec:
                compilerArgs.append("DO_OFFLOAD=1")
            # Eospac depends on fcommon behavior
            #   but gcc@10 flipped to default fno-common
            if "%gcc@10:" in spec:
                compilerArgs.append("CFLAGS=-fcommon")
            if self.run_tests:
                make("check", *compilerArgs)
            make(
                "install",
                "prefix={0}".format(prefix),
                "INSTALLED_LIBRARY_DIR={0}".format(prefix.lib),
                "INSTALLED_INCLUDE_DIR={0}".format(prefix.include),
                "INSTALLED_EXAMPLE_DIR={0}".format(prefix.example),
                "INSTALLED_BIN_DIR={0}".format(prefix.bin),
                *compilerArgs,
            )
        # fix conflict with linux's getopt for 6.4.0beta.2
        if spec.satisfies("@6.4.0beta.2"):
            with working_dir(prefix.bin):
                move("getopt", "driver_getopt")
