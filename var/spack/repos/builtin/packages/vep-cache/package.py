# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class VepCache(Package):
    """Separate installation and management for the Ensembl Variant Effect Predictor (vep)"""

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/112/INSTALL.pl"
    list_url = "https://github.com/Ensembl/ensembl-vep/tags"
    #https://ftp.ensembl.org/pub/release-111/variation/indexed_vep_cache/homo_sapiens_vep_111_GRCh37.tar.gz

    def url_for_version(self, version):
        major = version.up_to(1)
        url = f"https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/{major}/INSTALL.pl"
        vep = Spec(f"vep+installer@{major}")
        return vep.package.vep_installer_path if vep.installed else url

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="github_user1")

    vep_versions = [
        ("112", "f0f54759be885b3d0f10c2a1210c7d9b137ed548cecc0df6ed2d44df25c25b3a"),
        ("111", "1fa3510fdfb67d5c116dca9cd412744cb0dba9e0cd65e71761eabe385ca41aa1"),
        ("110", "e04572d4bf98e1392e31a274f1bb67b26a60689025183308dd90cc5e27015392"),
    ]

    for major, sha in vep_versions:
        version(major, sha256=sha, expand=False)
        depends_on(f"vep+installer@{major}", type="build", when=f"@{major}")
        depends_on(f"vep@{major}", type="run", when=f"@{major}")

    variant("env", default=True)
    variant("fasta", default=True)
    variant(
        "type",
        values=["ensembl", "refseq", "merged"],
        default="ensembl"
    )
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
        when="species=homo_sapiens"
    )

    @property
    def vep(self):
        return self.spec['vep'].package

    @property
    def vep_cache_path(self):
        return self.vep.vep_share_path

    @property
    def vep_cache_config(self):
        spec = self.spec
        satisfies = spec.satisfies
        variants = spec.variants
        cache_version = spec.version.up_to(1)
        vep_version = self.vep.version.up_to(1)

        if cache_version == "default":
            cache_version = vep_version

        cache_type = variants['type'].value
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

    def setup_run_environment(self, env):
        if self.spec.satisfies("+env"):
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
        auto = "cf" if self.spec.satisfies("+fasta") else "c"
        args = [
            "--AUTO", auto,
            "--NO_UPDATE",
            "--NO_TEST",
        ]
        args += self.cache_installer_args()
        return args

    def install(self, spec, prefix):
        mkdirp(self.vep_cache_path)
        installer = which(self.vep.vep_installer_path)
        installer(*self.installer_args())
