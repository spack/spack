# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Edm4hep(CMakePackage):
    """Event data model of Key4hep."""

    homepage = "https://github.com/key4hep/EDM4hep"
    url = "https://github.com/key4hep/EDM4hep/archive/v00-01.tar.gz"
    git = "https://github.com/key4hep/EDM4hep.git"

    maintainers("vvolkl", "jmcarcell", "tmadlener")

    tags = ["hep", "key4hep"]

    license("Apache-2.0")

    version("main", branch="main")
    version("0.10.5", sha256="003c8e0c8e1d1844592d43d41384f4320586fbfa51d4d728ae0870b9c4f78d81")
    version(
        "0.10.4",
        sha256="76d51947525bc8a27b62f567033255da2e632d42d07a32ff578887948d56bd6f",
        deprecated=True,
    )
    version("0.10.3", sha256="0ba5e4e90376f750f9531831909160e3d7b9c2d1f020d7556f0d3977b7eaafcc")
    version("0.10.2", sha256="c22c5c2f0fd1d09da9b734c1fa7ee546675fd2b047406db6ab8266e7657486d2")
    version("0.10.1", sha256="28a3bd4df899309b14ec0d441f8b6ed0065206a08a0018113bb490e9d008caed")
    version("0.10", sha256="a95c917c19793cfad6b0959854a653c5ce698c965598cabd649d544da07712c0")

    _cxxstd_values = ("17", "20")
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@3.3:", type="build")
    depends_on("cmake@3.23:", type="build", when="@0.10.3:")
    depends_on("python", type="build")

    depends_on("root@6.08:")
    depends_on("nlohmann-json@3.10:")
    depends_on("podio@0.15:")
    for _std in _cxxstd_values:
        depends_on("podio cxxstd=" + _std, when="cxxstd=" + _std)

    depends_on("py-jinja2", type="build")
    depends_on("py-pyyaml", type="build")

    depends_on("hepmc3", type="test")
    depends_on("heppdt", type="test")
    depends_on("catch2@3.0.1:", type="test")

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append(self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value))
        args.append(self.define("BUILD_TESTING", self.run_tests))
        return args

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["edm4hep"].libs.directories[0])
        env.prepend_path("PYTHONPATH", self.prefix.python)

    def url_for_version(self, version):
        """Translate version numbers to ilcsoft conventions.
        in spack, the convention is: 0.1 (or 0.1.0) 0.1.1, 0.2, 0.2.1 ...
        in ilcsoft, releases are dashed and padded with a leading zero
        the patch version is omitted when 0
        so for example v01-12-01, v01-12 ...
        :param self: spack package class that has a url
        :type self: class: `spack.PackageBase`
        :param version: version
        :type param: str
        """
        base_url = self.url.rsplit("/", 1)[0]

        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version

        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = "v%02d-%02d.tar.gz" % (major, minor)
        else:
            version_str = "v%02d-%02d-%02d.tar.gz" % (major, minor, patch)

        return base_url + "/" + version_str
