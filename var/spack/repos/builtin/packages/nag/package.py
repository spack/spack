# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path

from spack.package import *


class Nag(Package, CompilerPackage):
    """The NAG Fortran Compiler."""

    homepage = "https://www.nag.com/nagware/np.asp"
    maintainers("skosukhin")

    version("7.2.7203", sha256="775e2a10329bcf1c0ba35adb73d49db11b76698ede1f4ae070177216c9ee6e1e")
    version(
        "7.2.7200",
        sha256="3c2179e073d6cf2aadaeaf9a6a5f3b7f1fdcfb85b99c6fb593445b28ddd44880",
        url="file://{0}/npl6a72na_amd64.tgz".format(os.getcwd()),
        deprecated=True,
    )
    version("7.1.7125", sha256="738ed9ed943ebeb05d337cfdc603b9c88b8642b3d0cafea8d2872f36201adb37")
    version(
        "7.1.7101",
        sha256="18640737b232cebeb532ba36187675cdaf36d5b1fc235a780fc9e588c19a3ed2",
        url="file://{0}/npl6a71na_amd64.tgz".format(os.getcwd()),
        deprecated=True,
    )
    version("7.0.7048", sha256="6d509208533d79139e5a9f879b7b93e7b58372b78d404d51f35e491ecbaa54c7")
    version("6.2.6252", sha256="9b60f6ffa4f4be631079676963e74eea25e8824512e5c864eb06758b2a3cdd2d")
    version(
        "6.1.6136",
        sha256="32580e0004e6798abf1fa52f0070281b28abeb0da2387530a4cc41218e813c7c",
        url="file://{0}/npl6a61na_amd64.tgz".format(os.getcwd()),
        deprecated=True,
    )

    depends_on("fortran", type="build")  # generated

    # Licensing
    license_required = True
    license_comment = "!"
    license_files = ["lib/nag.key"]
    license_vars = ["NAG_KUSARI_FILE"]
    license_url = "http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt"

    # The installation script erroneously revokes execute permissions for the
    # installation directory of the man pages and therefore fails to copy all the files:
    patch("chmod_man.patch", when="@7.0:")

    def url_for_version(self, version):
        # TODO: url and checksum are architecture dependent
        # TODO: We currently only support x86_64
        url = "https://www.nag.com/downloads/impl/npl6a{0}na_amd64.tgz"
        return url.format(version.up_to(2).joined)

    def install(self, spec, prefix):
        # Set installation directories
        os.environ["INSTALL_TO_BINDIR"] = prefix.bin
        os.environ["INSTALL_TO_LIBDIR"] = prefix.lib
        os.environ["INSTALL_TO_MANDIR"] = prefix.share.man.man

        # Run install script
        os.system("./INSTALLU.sh")

    def setup_run_environment(self, env):
        env.set("F77", self.prefix.bin.nagfor)
        env.set("FC", self.prefix.bin.nagfor)

    compiler_languages = ["fortran"]
    fortran_names = ["nagfor"]
    compiler_version_regex = r"NAG Fortran Compiler Release (\d+).(\d+)\(.*\) Build (\d+)"
    compiler_version_argument = "-V"

    # Unlike other compilers, the NAG compiler passes options to GCC, which
    # then passes them to the linker. Therefore, we need to doubly wrap the
    # options with '-Wl,-Wl,,'
    rpath_arg = "-Wl,-Wl,,-rpath,,"
    linker_arg = "-Wl,-Wl,,"
    disable_new_dtags = ""
    enable_new_dtags = ""
    debug_flags = ["-g", "-gline", "-g90"]
    opt_flags = ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"]

    link_paths = {"fortran": os.path.join("nag", "nagfor")}

    # NAG does not support a flag that would enable verbose output and
    # compilation/linking at the same time (with either '-#' or '-dryrun'
    # the compiler only prints the commands but does not run them).
    # Therefore, the only thing we can do is to pass the '-v' argument to
    # the underlying GCC. In order to get verbose output from the latter
    # at both compile and linking stages, we need to call NAG with two
    # additional flags: '-Wc,-v' and '-Wl,-v'. However, we return only
    # '-Wl,-v' for the following reasons:
    #   1) the interface of this method does not support multiple flags in
    #      the return value and, at least currently, verbose output at the
    #      linking stage has a higher priority for us;
    #   2) NAG is usually mixed with GCC compiler, which also accepts
    #      '-Wl,-v' and produces meaningful result with it: '-v' is passed
    #      to the linker and the latter produces verbose output for the
    #      linking stage ('-Wc,-v', however, would break the compilation
    #      with a message from GCC that the flag is not recognized).
    #
    # This way, we at least enable the implicit rpath detection, which is
    # based on compilation of a C file (see method
    # spack.compiler._compile_dummy_c_source): in the case of a mixed
    # NAG/GCC toolchain, the flag will be passed to g++ (e.g.
    # 'g++ -Wl,-v ./main.c'), otherwise, the flag will be passed to nagfor
    # (e.g. 'nagfor -Wl,-v ./main.c' - note that nagfor recognizes '.c'
    # extension and treats the file accordingly). The list of detected
    # rpaths will contain only GCC-related directories and rpaths to
    # NAG-related directories are injected by nagfor anyway.
    verbose_flag = "-Wl,-v"

    openmp_flag = "-openmp"

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        return str(self.spec.prefix.bin.nagfor)
