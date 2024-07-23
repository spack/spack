# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGleanParser(PythonPackage):
    """Parser tools for Mozilla's Glean telemetry."""

    homepage = "https://mozilla.github.io/glean_parser/"
    pypi = "glean_parser/glean_parser-14.1.2.tar.gz"

    license("MPL-2.0", checked_by="teaguesterling")

    version("14.1.2", sha256="38be7d4e0fab0f83340e3427914e08a8631c7fab088a8c60e9b543cab6ea830c")
    version("14.0.1", sha256="3e9e5f99ad8592300e364b70d6247b21c445774a73a2ad274677fb58a0065809")
    version("14.0.0", sha256="94a54b638a3eaff43a37b2ff05fb61c5df4e79899a1dbbcfbc708996eb69199d")
    version("13.0.1", sha256="feead4cbec6930ed38a48df5bae9eb4ee486bb4026ddf2f3206b85f80279d1e7")

    depends_on("py-semver@2.13.0:")
    depends_on("py-appdirs@1.4:")
    depends_on("py-click@7:")
    depends_on("py-diskcache@4:")
    depends_on("py-jinja2@2.10.1:")
    depends_on("py-jsonschema@3.0.2:")
    depends_on("py-pyyaml@5.3.1:")

    depends_on("py-setuptools-scm@7:", type="build")
