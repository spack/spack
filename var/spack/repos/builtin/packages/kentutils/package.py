# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities"""

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    version("465", sha256="eef17b1f3182d1d9dc99b5c73a6b0468d5d3bd80470f25d3f7706cc1372e04b0")
    version("460", sha256="b955e56ee880074521ef1ab1371491f47e66dc6fdd93b05328386dd675a635fa")
    # This version isn't present in the archive any more
    # Might be worth changing url to: https://github.com/ucscGenomeBrowser/kent-core/tags/...
    version(
        "459",
        sha256="0b6e89a183e6385c713cf010a7aeead9da6626d8d2f78c363a4f1bc56ccccebb",
        deprecated=True,
    )

    variant("libs", default=True, description="Install jk*.a libraries")
    variant("force_mysql", default=False, description="Force MySQL over MariaDB")

    with default_args(type=("build", "link", "run")):
        depends_on("libpng")
        depends_on("openssl")
        depends_on("libuuid")
        depends_on("mysql-client")
        depends_on("zlib-api")
        depends_on("freetype")
        depends_on("libiconv")

    # The bgzip.c bug present inother packages is present in kent/src/htslib/bgzf.c
    # Conflicting line: assert(compressBound(BGZF_BLOCK_SIZE) < BGZF_MAX_BLOCK_SIZE);
    # We can patch this by removing the assertion, but there are still performance issues
    # See: https://github.com/samtools/htslib/issues/1257
    conflicts("zlib-ng")

    # Does not add a link to mysql_config, which is required for compilation
    conflicts("mariadb-c-client")

    # MariaDB can take a very long time to compile if you just need the c client
    conflicts("mariadb", when="+force_mysql")

    def flag_handler(self, name, flags):
        if name == "ldflags":
            flags.append(f'{self.spec["libiconv"].libs.ld_flags}')
        return (flags, None, None)

    @property
    def kent_platform(self):
        # There has to be an easier way to get this
        return self.spec.architecture.target.microarchitecture.family.name

    @property
    def machtype(self):
        # This is hard-coded in the Makefile, but doesn't cover all files
        # for those we need to use the platform
        return "local"

    def install_libs_from_stage(self, prefix):
        # Dependent packages expect things in the source tree, but we don't
        # want to copy all of the compilation artifacts in
        # Would it be better to just patch an install target into the makefile?
        src_prefix = "kent/src"

        lib_dir = join_path("lib", self.machtype)
        parasol = join_path("parasol/lib", self.machtype)
        altsplice = join_path("hg/altSplice/lib", self.machtype)
        htslib = "htslib"

        for lib_prefix in [lib_dir, parasol, altsplice, htslib, "include"]:
            mkdirp(join_path(prefix, lib_prefix))

        install_tree(join_path(src_prefix, "inc"), prefix.include)
        
        lib_names = ["jkweb.a", "jkOwnLib.a", "jkhgap.a", "jkhgapcgi.a"]
        libs = [join_path(lib_dir, name) for name in lib_names]
        libs += [
            join_path(parasol, "paralib.a"),
            join_path(altsplice, "libSpliceGraph.a"),
            join_path(htslib, "libhts.a"),
        ]

        for lib in libs:
            install(join_path("kent/src", lib), join_path(prefix, lib))

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        if spec.satisfies("+libs"):
            self.install_libs_from_stage(prefix)
