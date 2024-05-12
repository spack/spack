# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vep(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://github.com/Ensembl/ensembl-vep/archive/release/111.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="github_user1")

    version("111.0", sha256="9cb326a1fa0054ce1a417f8fd4f2325ba605c40ec10eefbf87f461c264a89407")
    version("110.0", sha256="391a1fe50139064c1044c09e013bb21437933d677537b5d3336807f3b131fb51")
    
    depends_on("gcc")
    depends_on("gmake")
    depends_on("perl@5.10:")
    extends("perl")

    depends_on("perl-archive-zip")
    depends_on("perl-dbd-mysql")
    depends_on("perl-dbi")
    depends_on("perl-bio-db-hts")
    depends_on("perl-json", when="+json")
    depends_on("perl-set-intervaltree", when="+nearest")
    depends_on("perl-perlio-gzip", when="+gzip")
    depends_on("perl-bioperl@1.6:", when="~bundled_bioperl")
    depends_on("htslib@1.9", when="~bundled_htslib")

    variant("installer", default=True)
    variant("utility_scripts", default=True)

    # Optional dependencies
    variant("json", default=True)
    variant("nearest", default=True)
    variant("gzip", default=True)

    # Bundled versions
    variant("bundled_bioperl", default=False)
    variant("bundled_htslib", default=False)

    @property
    def vep_lib_path(self):
        return self.prefix.lib.perl5

    @property
    def vep_share_path(self):
        return self.prefix.share.vep

    @property
    def vep_scripts_path(self):
        return self.vep_share_path.scripts

    @property
    def vep_installer_path(self):
        return f"{self.vep_scripts_path.INSTALL}.pl"

    def setup_run_environment(self, env):
        env.set("VEP_HOME", self.home)
        if self.spec.satisfies("+htslib"):
            env.prepend_path("PATH", self.vep_lib_path.htslib)

    def installer_args(self):
        auto = "a"
        args = [
            "--DESTDIR", f"{self.vep_lib_path}",
            "--NO_UPDATE",
            "--NO_TEST",
        ]
        if self.spec.satisfies("~bundled_htslib"):
           args += ["--NO_HTSLIB"]
        if self.spec.satisfies("~bundled_bioperl"):
            args += ["--NO_BIOPERL"]
        args += ["--AUTO", auto]
        return args

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.vep_lib_path)
        mkdirp(self.vep_share_path)
        mkdirp(self.vep_scripts_path)
        with working_dir(self.stage.source_path):

            # Run really weird and awkward VEP installer
            if spec.satisfies("+installer"):
                installer_script = "./INSTALL.pl"
                installer = which(installer_script)
                installer(*self.installer_args())

                # We save this so it can be used later to update caches
                install(installer_script, self.vep_installer_path)

            install_tree("modules", self.vep_lib_path)

            # Install VEP script
            # VEP requires specifying a bunch of paths when using the cache
            # this is really difficult to do with spack's generated prefixes
            # so we optionally have a wrapper that we can install in the 
            # patch section
            install("vep", prefix.bin.vep)
            
            # Manually install auxilary scripts if requested
            if self.spec.satisfies("+utility_scripts"):
                install("filter_vep", prefix.bin.filter_vep)
                install("haplo", prefix.bin.haplo)
                install("variant_recoder", prefix.bin.variant_recoder)
                install("convert_cache.pl", self.vep_scripts_path)

