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
    version("464", sha256="24e20fe68e2a2894d802c87662f69a62f71b3c15fafb2e4d6c3c425c63638bb2")
    version("460", sha256="b955e56ee880074521ef1ab1371491f47e66dc6fdd93b05328386dd675a635fa")
    version("455", sha256="e458cadad7c4a5c1b8385edafffa1b29380ac725a0c20535bf5a3bab99fe80db")
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

    # The bgzip.c bug present in other packages is present in kent/src/htslib/bgzf.c
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
    def machtype(self):
        # This is hard-coded in the Makefile and included here for reference
        # and to make it adjustable if we need to adjust this in the future
        return "local"

    def install_libs_from_stage(self, prefix):
        # Dependent packages expect things in the source tree, but we don't
        # want to copy all of the compilation artifacts in so we'll do them
        # manually instead of leaving the build directory around
        import os

        src_prefix = "kent/src"

        # I'm not sure if all dependents look for inc or some look in .../include
        install_tree(join_path(src_prefix, "inc"), join_path(prefix, "inc"))

        libs = [
            f"lib/{self.machtype}/jkweb.a",
            f"lib/{self.machtype}/jkOwnLib.a",
            f"lib/{self.machtype}/jkhgap.a",
            f"lib/{self.machtype}/jkhgapcgi.a",
            f"parasol/lib/{self.machtype}/paralib.a",
            f"hg/altSplice/lib/{self.machtype}/libSpliceGraph.a",
            "htslib/libhts.a",
        ]

        for lib in libs:
            src = join_path(src_prefix, lib)
            dest = join_path(prefix, lib)
            mkdirp(os.path.dirname(dest))
            install(src, dest)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        if spec.satisfies("+libs"):
            self.install_libs_from_stage(prefix)
