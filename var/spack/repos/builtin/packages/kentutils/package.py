# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kentutils(MakefilePackage):
    """Jim Kent command line bioinformatic utilities and libraries"""

    homepage = "https://genome.cse.ucsc.edu/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v453.src.tgz"

    maintainers("teaguesterling")

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
    variant(
        "htslib",
        default=False,
        description="Build and use bundled htslib (Careful: may lead to unexpected failures)",
        sticky=True,
    )

    with default_args(type=("build", "link", "run")):
        depends_on("libpng")
        depends_on("openssl")
        depends_on("uuid")
        depends_on("mysql-client")
        depends_on("zlib-api")
        depends_on("freetype")
        depends_on("libiconv")
        depends_on("htslib+pic", when="~htslib+libs")

    # The bgzip.c bug present in other packages is present in kent/src/htslib/bgzf.c
    # Conflicting line: assert(compressBound(BGZF_BLOCK_SIZE) < BGZF_MAX_BLOCK_SIZE);
    # We can patch this by removing the assertion, but there are still performance issues
    # See: https://github.com/samtools/htslib/issues/1257
    conflicts("zlib-ng")

    # Does not add a link to mysql_config, which is required for compilation
    conflicts("mariadb-c-client")

    # MariaDB can take a very long time to compile if you just need the c client
    conflicts("mariadb", when="+force_mysql")

    # MySQL pointer/integer conversion issue
    patch("fix-mysql-options-gcc13.patch", when="%gcc@13: ^mysql")
    # MySQL build flags improperly states the zlib-api library
    patch("mysql-zlib-workaround.patch", when="%gcc ^mysql")

    def flag_handler(self, name, flags):
        if name == "ldflags":
            flags.append(f'{self.spec["libiconv"].libs.ld_flags}')
        elif name == "cflags" and self.spec.satisfies("+libs"):
            flags.append("-fPIC")
        return (flags, None, None)

    @property
    def machtype(self):
        # This is hard-coded in the Makefile and included here for reference
        # and to make it adjustable if we need to adjust this in the future
        return "local"

    @property
    def headers(self):
        headers = []
        if self.spec.satisfies("+libs"):
            headers.extend(find_headers("*", self.prefix.inc, recursive=True))
        if self.spec.satisfies("+htslib+libs"):
            headers.extend(find_headers("*", self.prefix.htslib, recursive=True))
        return HeaderList(headers)

    @property
    def libs(self):
        return LibraryList([join_path(self.prefix, lib) for lib in self.local_libs])

    @property
    def local_libs(self):
        libs = []
        if self.spec.satisfies("+libs"):
            libs.extend(
                [
                    f"{self.machlib}/jkweb.a",
                    f"{self.machlib}/jkOwnLib.a",
                    f"{self.machlib}/jkhgap.a",
                    f"{self.machlib}/jkhgapcgi.a",
                    f"hg/altSplice/{self.machlib}/libSpliceGraph.a",
                ]
            )
        if self.spec.satisfies("+htslib+libs"):
            libs.append("htslib/libhts.a")
        return LibraryList(libs)

    @property
    def machlib(self):
        return f"lib/{self.machtype}"

    @property
    def lib_dir(self):
        return join_path(self.prefix, self.machlib)

    def install_libs_from_stage(self, spec, prefix):
        # Dependent packages expect things in the source tree, but we don't
        # want to copy all of the compilation artifacts in so we'll do them
        # manually instead of leaving the build directory around
        import os

        src_prefix = "kent/src"

        def install_kent(path, tree):
            src = join_path(src_prefix, path)
            dest = join_path(prefix, path)
            mkdirp(os.path.dirname(dest))
            if tree:
                install_tree(src, dest)
            else:
                install(src, dest)

        install_kent("inc", tree=True)
        if spec.satisfies("+htslib"):
            install_kent("htslib/htslib", tree=True)

        for lib in self.local_libs:
            install_kent(lib, tree=False)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        if spec.satisfies("+libs"):
            self.install_libs_from_stage(spec, prefix)
