# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAlphafoldColabfold(PythonPackage, CudaPackage):
    """An implementation of the inference pipeline of AlphaFold v2.3.1.
    This is a completely new model that was entered as AlphaFold2 in CASP14
    and published in Nature. This package contains patches for colabfold."""

    homepage = "https://pypi.org/project/alphafold-colabfold/#description"
    pypi = "alphafold-colabfold/alphafold-colabfold-2.3.5.tar.gz"
    git = "https://github.com/sokrypton/alphafold"

    version("latest", branch="main")
    version("2.3.5", sha256="92a01f96851b4c2897c3fc1a083dc215cffe318ab06bdbb3186b7d41a5e72e4b")

    conflicts("platform=darwin", msg="alphafold is only supported on Linux")

    # lots of hints on versions and patching taken from docker/Dockerfile
    # and requirements.txt
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.13.0:", type=("build", "run"), when="@2.1.1")
    depends_on("py-absl-py@1.0.0:", type=("build", "run"), when="@2.2.4:")
    depends_on("py-biopython@1.79:", type=("build", "run"))
    depends_on("py-chex@0.0.7:", type=("build", "run"))
    depends_on("py-dm-haiku@0.0.4:", type=("build", "run"), when="@2.1.1")
    depends_on("py-dm-haiku@0.0.7:", type=("build", "run"), when="@2.2.4:")
    depends_on("py-dm-tree@0.1.6:", type=("build", "run"))
    depends_on("py-docker", type=("build", "run"))
    depends_on("py-immutabledict@2.0.0:", type=("build", "run"))
    depends_on("py-jax@0.2.14:", type=("build", "run"), when="@2.1.1")
    depends_on("py-jax@0.3.17:", type=("build", "run"), when="@2.2.4:")
    depends_on("py-ml-collections@0.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.19.5:", type=("build", "run"), when="@2.1.1")
    depends_on("py-numpy@1.21.6:", type=("build", "run"), when="@2.2.4:")
    depends_on("py-pandas@1.3.4:", type=("build", "run"))
    depends_on("py-protobuf@3.19:", type=("build", "run"), when="@2.2.4:")
    depends_on("py-scipy@1.7.0:", type=("build", "run"))
    depends_on("py-pdbfixer@1.7", type=("build", "run"))
    depends_on("py-tensorflow@2.5:", type=("build", "run"), when="@2.1.1")
    depends_on("py-tensorflow@2.9:", type=("build", "run"), when="@2.2.4:")
#    depends_on(
#        "openmm@7.5.1+cuda",
#        type="run",
#        patches=[
#            patch(
#                "https://raw.githubusercontent.com/deepmind/alphafold/main/docker/openmm.patch",
#                sha256="a5a0ced820f3ecc56ae634c3111f80614863559b0587954a2658c8d4b2a07ae3",
#                working_dir="wrappers/python",
#                level=0,
#            )
#        ],
#    )
    depends_on("hmmer", type="run")
    depends_on("kalign2", type="run")
    depends_on("hh-suite", type="run")
    depends_on("aria2", type="run")

    resource(
        name="chemprops",
        url="https://git.scicore.unibas.ch/schwede/openstructure/-/raw/7102c63615b64735c4941278d92b554ec94415f8/modules/mol/alg/src/stereo_chemical_props.txt",
        destination="",
        sha256="24510899eeb49167cffedec8fa45363a4d08279c0c637a403b452f7d0ac09451",
        expand=False,
        placement="chemprops",
    )

    #patch(
    #    url_or_filename="https://github.com/sokrypton/alphafold/commit/1f04253c620703d6768b20987b3b5e075314095f.patch",
    #    sha256="b29d56b236e65ae609b7e4edf7e72c2b9a3a7ff048c9939950cab12192ca0e43",
    #    when="@2.3.5 ^jax@0.3.26:"
    #)

    @run_after("install")
    def install_scripts(self):
        mkdirp(self.prefix.bin)
        shebang = "#!{0}\n".format(self.spec["python"].command)
        for fname in glob.glob("run_alphafold*.py"):
            destfile = join_path(self.prefix.bin, fname)
            with open(fname, "r") as src:
                srcdata = src.read()
            with open(destfile, "w") as dest:
                dest.write(shebang + srcdata)
                set_executable(destfile)

        python_dir = join_path(self.prefix, python_platlib, "alphafold", "common")
        install("chemprops/stereo_chemical_props.txt", python_dir)
        install_tree("scripts", self.prefix.scripts)
