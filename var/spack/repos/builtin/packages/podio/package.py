# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Podio(CMakePackage):
    """PODIO, or plain-old-data I/O, is a C++ library to support the creation
    and handling of data models in particle physics."""

    homepage = "https://github.com/AIDASoft/podio"
    url = "https://github.com/AIDASoft/podio/archive/v00-09-02.tar.gz"
    git = "https://github.com/AIDASoft/podio.git"

    maintainers("vvolkl", "drbenmorgan")

    tags = ["hep", "key4hep"]

    version("master", branch="master")
    version("0.16.2", sha256="faf7167290faf322f23c734adff19904b10793b5ab14e1dfe90ce257c225114b")
    version("0.16.1", sha256="23cd8dfd00f9cd5ae0b473ae3279fa2c22a2d90fb6c07b37d56e63a80dd76ab2")
    version("0.16", sha256="4e149c2c9be9f9ca3a6d863498bb0f642dda1a43a19ac1afe7f99854ded5c510")
    version("0.15", sha256="6c1520877ba1bce250e35a2a56c0a3da89fae0916c5ed7d5548d658237e067d9")
    version("0.14.3", sha256="2a7a405dedc7f6980a0aad7df87b427a1f43bcf6d923a9bcce1698fd296359f7")
    version(
        "0.14.1",
        sha256="361ac3f3ec6f5a4830729ab45f96c19f0f62e9415ff681f7c6cdb4ebdb796f72",
        deprecated=True,
    )
    version(
        "0.14",
        sha256="47f99f1190dc71d6deb52a2b1831250515dbd5c9e0f263c3c8553ffc5b260dfb",
        deprecated=True,
    )
    version(
        "0.13.2",
        sha256="645f6915ca6f34789157c0a9dc8b0e9ec901e019b96eb8a68fb39011602e92eb",
        deprecated=True,
    )
    version(
        "0.13.1",
        sha256="2ae561c2a0e46c44245aa2098772374ad246c9fcb1956875c95c69c963501353",
        deprecated=True,
    )
    version(
        "0.13",
        sha256="e9cbd4e25730003d3706ad82e28b15cb5bdc524a78b0a26e90b89ea852101498",
        deprecated=True,
    )
    version(
        "0.12",
        sha256="1729a2ce21e8b307fc37dfb9a9f5ae031e9f4be4992385cf99dba3e5fdf5323a",
        deprecated=True,
    )
    version(
        "0.11",
        sha256="4b2765566a14f0ddece2c894634e0a8e4f42f3e44392addb9110d856f6267fb6",
        deprecated=True,
    )
    version(
        "0.10",
        sha256="b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2",
        deprecated=True,
    )
    version(
        "0.9.2",
        sha256="8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240",
        deprecated=True,
    )
    version(
        "0.9",
        sha256="3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f",
        deprecated=True,
    )
    version(
        "0.8",
        sha256="9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327",
        deprecated=True,
    )

    variant(
        "cxxstd",
        default="17",
        values=("17", conditional("20", when="@0.15:")),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant("sio", default=False, description="Build the SIO I/O backend")

    # cpack config throws an error on some systems
    patch("cpack.patch", when="@:0.10.0")
    patch("dictloading.patch", when="@0.10.0")
    patch("python-tests.patch", when="@:0.14.0")

    depends_on("root@6.08.06: cxxstd=17", when="cxxstd=17")
    depends_on("root@6.25.02: cxxstd=20", when="cxxstd=20")

    depends_on("cmake@3.8:", type="build")
    depends_on("python", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-jinja2@2.10.1:", type=("build", "run"), when="@0.12.0:")
    depends_on("sio", type=("build", "link"), when="+sio")
    depends_on("catch2@3.0.1:", type=("test"), when="@0.13:")

    conflicts("+sio", when="@:0.12", msg="sio support requires at least podio@0.13")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SIO", "sio"),
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["podio"].libs.directories[0])
        if "+sio" in self.spec and self.version >= Version("0.16"):
            # sio needs to be on LD_LIBRARY_PATH for ROOT to be able to
            # dynamicaly load the python bindings library
            env.prepend_path("LD_LIBRARY_PATH", self.spec["sio"].libs.directories[0])

        if self.spec.satisfies("@0.16.1:"):
            # Frame header needs to be available for python bindings
            env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["podio"].libs.directories[0])
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

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
