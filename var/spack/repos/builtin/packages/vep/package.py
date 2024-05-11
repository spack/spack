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
#     spack install vep
#
# You can edit this file again by typing:
#
#     spack edit vep
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Vep(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://github.com/Ensembl/ensembl-vep/archive/release/111.zip"

    maintainers("teaguesterling")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

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
    depends_on("perl-bioperl", when="~bioperl")
    depends_on("htslib", when="~htslib")

    variant("installer", default=True)
    variant("utility_scripts", default=True)

    # Optional dependencies
    variant("json", default=True)
    variant("nearest", default=True)
    variant("gzip", default=True)

    # Bundled versions
    variant("bioperl", default=False)
    variant("htslib", default=False)

    # Cache Downloading
    variant("cache", default=True, when="+installer")
    with default_args(when="+cache"):
        variant("cacheenviron", default=True)
        variant("cacheversion",
            values=["default", "111", "110"],
            default="default")
        variant("cachetype",
            values=["ensembl", "refseq", "merged"],
            default="ensembl")
        variant("wrapper", default=True)
        variant("fasta", default=True)
        variant(
            "species", 
            values=["homo_sapiens", "mouse", "all"], 
            default="homo_sapiens",
            multi=True
        ) 
        variant(
            "assembly", 
            values=["grch37", "grch38"], 
            default="grch38",
            when="+cache species=homo_sapiens"
        )

    @property
    def vep_lib_path(self):
        return self.prefix.lib.site_perl

    @property
    def vep_cache_path(self):
        return self.prefix.share.vep

    def setup_run_environment(self, env):
        env.set("VEP_HOME", self.home)
        if self.spec.satisfies("+cacheenviron"):
            cache = self.vep_cache_config
            env.set("VEP_OFFLINE", "1")
            env.set("VEP_CACHE", "1")
            env.set("VEP_DIR", self.vep_cache_path)
            env.set("VEP_SPECIES", cache['default_species'])
            env.set("VEP_CACHE_VERSION", cache['version'])
            if cache["assembly"] is not None:
                env.set("VEP_ASSEMBLY", cache['assembly'])
            if cache["type"] == "refseq":
                env.set("VEP_REFSEQ", "1")
            if cache["type"] == "merged":
                env.set("VEP_MERGED", "1")
            if self.spec.satisfies("+fasta"):
                pass
        if self.spec.satisfies("+htslib"):
            env.prepend_path("PATH", self.vep_lib_path.htslib)

    @property
    def vep_cache_config(self):
        spec = self.spec
        satisfies = spec.satisfies
        variants = spec.variants
        vep_version = spec.version.up_to(1) 

        cache_version = variants['cacheversion'].value
        if cache_version == "default":
            cache_version = vep_version
        cache_type = variants['cachetype'].value
        species_names = variants['species'].value

        suffix = "" if cache_type == "ensembl" else f"_{cache_type}"
        species_cache = [f"{species}{suffix}" for species in species_names]

        if "homo_sapiens" in species_names:
            assembly = variants['assembly'].value
            assembly = assembly.replace("grch", "GRCh")
        else:
            assembly = None

        return {
            "dir": f"{self.vep_cache_path}",
            "version": f"{cache_version}",
            "type": f"{cache_type}",
            "species": [f"{name}" for name in species_names],
            "cache_species": species_cache,
            "default_species": f"{species_names[0]}",
            "assembly": f"{assembly}",
        }

    def cache_installer_args(self):
        cache = self.vep_cache_config
        args = [
            "--CACHEDIR", cache['dir'],
            "--CACHE_VERSION", cache['version'],
            "--SPECIES", ','.join(cache['cache_species']),
        ]
        if cache['assembly'] is not None:
            args += ["--ASSEMBLY", cache['assembly']]

        return args

    def installer_args(self):
        auto = "a"
        args = [
            "--DESTDIR", f"{self.vep_lib_path}",
            "--NO_UPDATE",
            "--NO_TEST",
        ]
        if self.spec.satisfies("~htslib"):
           args += ["--NO_HTSLIB"]
        if self.spec.satisfies("~bioperl"):
            args += ["--NO_BIOPERL"]
        if self.spec.satisfies("+cache"):
            auto += "cf" if self.spec.satisfies("+fasta") else "c"
            args += self.cache_installer_args()

        args += ["--AUTO", auto]
        return args

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.vep_lib_path)
        mkdirp(self.vep_cache_path)
        with working_dir(self.stage.source_path):

            # Run really weird and awkward VEP installer
            if spec.satisfies("+installer"):
                installer = which("./INSTALL.pl")
                installer(*self.installer_args())

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
                install("convert_cache.pl", prefix.bin.variant_recoder)





