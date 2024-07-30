# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class VepCache(Package):
    """Separate installation and management for the Ensembl Variant Effect Predictor (vep)"""

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/112/INSTALL.pl"
    list_url = "https://github.com/Ensembl/ensembl-vep/tags"

    def url_for_version(self, version):
        major = version.up_to(1)
        url = f"https://raw.githubusercontent.com/Ensembl/ensembl-vep/release/{major}/INSTALL.pl"
        vep = Spec(f"vep+installer@{major}")
        return vep.package.vep_installer_path if vep.installed else url

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    # The cache *should* be pinned to the VEP version, but there are reasons
    # that one may want to avoid that
    vep_versions = [
        ("112", "f0f54759be885b3d0f10c2a1210c7d9b137ed548cecc0df6ed2d44df25c25b3a"),
        ("111", "1fa3510fdfb67d5c116dca9cd412744cb0dba9e0cd65e71761eabe385ca41aa1"),
        ("110", "e04572d4bf98e1392e31a274f1bb67b26a60689025183308dd90cc5e27015392"),
    ]
    vep_species = [
        ("bos_taurus", ["UMD3.1"]),
        ("danio_rerio", ["GRCz11"]),
        ("homo_sapiens", ["GRCh37", "GRCh38"]),
        ("mus_musculus", ["GRCm38"]),
        ("rattus_norvegicus", ["Rnor_6.0"]),
    ]
    # We only need (and can) specify an assembly for humans
    vep_assembly_choices = [
        assembly
        for species, assemblies in vep_species
        for assembly in assemblies
        if species == "homo_sapiens"
    ]

    variant("installer", default=True, description="Use built-in VEP installer to download")
    variant("indexed", default=True, description="Use indexed cache")
    variant("env", default=True, description="Setup VEP environment variables for this cache")
    variant("fasta", default=True, description="Add FASTA files to the cache")
    variant(
        "type",
        values=["ensembl", "refseq", "merged"],
        default="ensembl",
        description="What reference genome source to retrieve the cache for",
    )
    variant(
        "species",
        values=[species for species, _ in vep_species],
        default="homo_sapiens",
        description="Which species to download the cache for (only one at a time)",
    )
    variant(
        "assembly",
        values=[assembly.lower() for assembly in vep_assembly_choices],
        default="grch38",
        when="species=homo_sapiens",
        description="Which assembly of genome to use (only needed for homo sapiens",
    )

    @staticmethod
    def get_resource_filename(major_version, species, assembly):
        return f"{species}_vep_{major_version}_{assembly}.tar.gz"

    @staticmethod
    def vep_cache_resource_args(version, species, assembly, indexed, dest=""):
        filename = "{species}_vep_{major_version}_{assembly}.tar.gz"
        dir_name = "indexed_vep_cache" if indexed else "vep"
        root = f"https://ftp.ensembl.org/pub/release-{version}/variation/{dir_name}"
        url = f"{root}/{filename}"

        when = [
            f"@{version}",
            "~installer",  # Only need these resources when we don't use the installer
            "+indexed" if indexed else "~indexed",  # Only need the appropriate indexed version
            f"species={species}",  # Only need the requested species
            # We only need to match the specified assembly for human assemblies
            f"assemlby={assembly}" if species == "homo_sapiens" else "",
        ]

        return {
            "name": filename,
            "url": url,
            "when": " ".join(when),
            "destination": dest,
            "expand": False,  # We'll expand this where it needs to go latere
        }

    for major, sha in vep_versions:
        version(major, sha256=sha, expand=False)
        depends_on(f"vep+installer@{major}", type="build", when=f"@{major}")
        depends_on(f"vep@{major}", type="run", when=f"@{major}")
        for species, assemblies in vep_species:
            for assembly in assemblies:
                resource(
                    **vep_cache_resource_args(
                        version=major, species=species, assembly=assembly, indexed=True
                    )
                )
                resource(
                    **vep_cache_resource_args(
                        version=major, species=species, assembly=assembly, indexed=False
                    )
                )

    @property
    def vep(self):
        return self.spec["vep"].package

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
        user_root = f"{self.vep_cache_path}"
        root = f"{self.prefix.share.vep}"

        if cache_version == "default":
            cache_version = vep_version

        indexed = satisfies("+indexed")
        cache_type = variants["type"].value
        species_name = variants["species"].value
        assembly_name = variants["assembly"].value

        species = f"{species_name}"
        suffix = "" if cache_type == "ensembl" else f"_{cache_type}"
        species_cache = f"{species_name}{suffix}"

        if "homo_sapiens" in species_name:
            assembly = assembly_name.replace("grch", "GRCh")
            cache_dir = join_path(species, f"{vep_version}_{assembly}")
        else:
            for check_species, assemblies in self.vep_species:
                if species == check_species:
                    assembly = assemblies[0]
                    break
            else:
                assembly = ""
            cache_dir = join_path(species, f"{vep_version}")

        return {
            "root": root,
            "user_root": user_root,
            "version": f"{cache_version}",
            "type": f"{cache_type}",
            "species": species,
            "cache_species": species_cache,
            "assembly": f"{assembly}",
            "indexed": indexed,
            "dir": cache_dir,
            "full_path": join_path(root, cache_dir),
        }

    def setup_run_environment(self, env):
        if self.spec.satisfies("+env"):
            cache = self.vep_cache_config
            env.set("VEP_OFFLINE", "1")
            env.set("VEP_CACHE", "1")
            env.set("VEP_DIR", cache["user_root"])
            env.set("VEP_SPECIES", cache["species"])
            env.set("VEP_CACHE_VERSION", cache["version"])
            if cache["assembly"] is not None:
                env.set("VEP_ASSEMBLY", cache["assembly"])
            if cache["type"] == "refseq":
                env.set("VEP_REFSEQ", "1")
            if cache["type"] == "merged":
                env.set("VEP_MERGED", "1")
            if self.spec.satisfies("+fasta"):
                pass

    def cache_installer_args(self):
        cache = self.vep_cache_config
        args = [
            "--CACHEDIR",
            cache["dir"],
            "--CACHE_VERSION",
            cache["version"],
            "--SPECIES",
            ",".join(cache["cache_species"]),
        ]
        if cache["assembly"] is not None:
            args += ["--ASSEMBLY", cache["assembly"]]

        return args

    def installer_args(self):
        auto = "cf" if self.spec.satisfies("+fasta") else "c"
        args = ["--AUTO", auto, "--NO_UPDATE", "--NO_TEST"]
        args += self.cache_installer_args()
        return args

    def install_with_installer(self):
        installer = which(self.vep.vep_installer_path)
        installer(*self.installer_args())

    @property
    def stub_file_name(self):
        cache = self.vep_cache_config
        return "_".join(
            [".vep-cache", cache["version"], cache["cache_species"], cache["assembly"]]
        )

    def patch(self):
        with open(self.stub_file_name, "w") as f:
            f.write(str(self.spec))

    def install(self, spec, prefix):
        cache = self.vep_cache_config
        mkdirp(cache["root"])
        if not os.path.exists(cache["full_path"]):
            if spec.satisfies("+installer"):
                self.install_with_installer()
            else:
                tarball = self.get_resource_filename(
                    version=cache["version"],
                    species=cache["species"],
                    assembly=cache["assembly"],
                    indexed=cache["indexed"],
                )
                tar = which("tar")
                tar("xzvf", tarball, "-C", cache["root"])
        install(self.stub_file_name, prefix)
