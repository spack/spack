# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Verible(Package):
    """The Verible project’s main mission is to parse SystemVerilog
    (IEEE 1800-2017) (as standardized in the [SV-LRM]) for a wide variety of
    applications, including developer tools.

    It was born out of a need to parse un-preprocessed source files, which is
    suitable for single-file applications like style-linting and formatting.
    In doing so, it can be adapted to parse preprocessed source files, which
    is what real compilers and toolchains require.

    The spirit of the project is that no-one should ever have to develop a
    SystemVerilog parser for their own application, because developing a
    standard-compliant parser is an enormous task due to the syntactic
    complexity of the language. Verible’s parser is also regularly tested
    against an ever-growing suite of (tool-independent) language compliance
    tests at https://symbiflow.github.io/sv-tests/.

    A lesser (but notable) objective is that the language-agnostic components
    of Verible be usable for rapidly developing language support tools for
    other languages."""

    homepage = "https://chipsalliance.github.io/verible"
    git = "https://github.com/chipsalliance/verible.git"

    license("BSD-3-Clause")

    version("master", branch="master")

    version(
        "0.0.3539",
        sha256="e93c9638dac7d314cea506d483b0f078b80aa6837afa74db68ace322b0dbba31",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3539-g9442853c.tar.gz",
    )
    version(
        "0.0.3483",
        sha256="c40591813a7cf6b1a6f46f7e02d81526c999966c3ceb9a67c5542234cf49dddb",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3483-ga4d61b11.tar.gz",
    )
    version(
        "0.0.3430",
        sha256="580ab39c82da9f67523658c0bb0859e2b6c662f7c06855859f476eeedd92a7e0",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3430-g060bde0f.tar.gz",
    )
    version(
        "0.0.3428",
        sha256="2b83497662b890f875bfe859175aa8e4b87db6e6a177ad08a0694002b8767cb0",
        url="https://github.com/chipsalliance/verible/archive/refs/tags/v0.0-3428-gcfcbb82b.tar.gz",
    )

    maintainers("davekeeshan")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("bazel", type="build")

    conflicts("%gcc@:8", msg="Only works with gcc9 and above")

    def install(self, spec, prefix):
        bazel("build", "-c", "opt", "//...")
        bazel("run", "-c", "opt", ":install", "--", prefix.bin)
