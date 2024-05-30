# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    maintainers("vvolkl", "drbenmorgan", "jmcarcell", "tmadlener")

    tags = ["hep", "key4hep"]

    version("master", branch="master")
    version("0.99", sha256="c823918a6ec1365d316e0a753feb9d492e28903141dd124a1be06efac7c1877a")
    version(
        "0.17.4",
        sha256="3ca86323c86e05e901f596a98fe84aeb2476ceed8c0b0e0b37049c23b903a9ad",
        deprecated=True,
    )
    version(
        "0.17.3",
        sha256="079517eba9c43d01255ef8acd88468c3ead7bb9d8fed11792e121bb481d54dee",
        deprecated=True,
    )
    version(
        "0.17.2",
        sha256="5b519335c4e1708f71ed85b3cac8ca81e544cc4572a5c37019ce9fc414c5e74d",
        deprecated=True,
    )
    version(
        "0.17.1",
        sha256="97d6c5f81d50ee42bf7c01f041af2fd333c806f1bbf0a4828ca961a24cea6bb2",
        deprecated=True,
    )
    version(
        "0.17",
        sha256="0c19f69970a891459cab227ab009514f1c1ce102b70e8c4b7d204eb6a0c643c1",
        deprecated=True,
    )
    version(
        "0.16.7",
        sha256="8af7c947e2637f508b7af053412bacd9218d41a455d69addd7492f05b7a4338d",
        deprecated=True,
    )
    version(
        "0.16.6",
        sha256="859f7cd16bd2b833bee9c1f33eb4cdbc2a0c2b1a48a853f67c30e8a0301d16df",
        deprecated=True,
    )
    version(
        "0.16.5",
        sha256="42135e4d0e11be6f0d88748799fa2ec985514d4b4c979a10a56a00a378f65ee0",
        deprecated=True,
    )
    version(
        "0.16.3",
        sha256="d8208f98496af68ca8d02d302f428aab510e50d07575b90c3477fff7e499335b",
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
    variant("rntuple", default=False, description="Build the RNTuple backend")

    depends_on("root@6.08.06: cxxstd=17", when="cxxstd=17")
    depends_on("root@6.28.04: +root7", when="+rntuple")
    depends_on("root@6.28:", when="@0.17:")
    for cxxstd in ("17", "20"):
        depends_on("root cxxstd={}".format(cxxstd), when="cxxstd={}".format(cxxstd))

    depends_on("cmake@3.12:", type="build")
    depends_on("python", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-jinja2@2.10.1:", type=("build", "run"))
    depends_on("sio", type=("build", "link"), when="+sio")
    depends_on("catch2@3.0.1:", type=("test"), when="@:0.16.5")
    depends_on("catch2@3.1:", type=("test"), when="@0.16.6:")
    depends_on("py-graphviz", type=("run"))
    depends_on("py-tabulate", type=("run", "test"), when="@0.16.6:")

    conflicts("+rntuple", when="@:0.16", msg="rntuple support requires at least podio@0.17")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_SIO", "sio"),
            self.define_from_variant("ENABLE_RNTUPLE", "rntuple"),
            self.define("CMAKE_CXX_STANDARD", self.spec.variants["cxxstd"].value),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        return args

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["podio"].libs.directories[0])
        if "+sio" in self.spec:
            # sio needs to be on LD_LIBRARY_PATH for ROOT to be able to
            # dynamicaly load the python bindings library
            env.prepend_path("LD_LIBRARY_PATH", self.spec["sio"].libs.directories[0])

        # Frame header needs to be available for python bindings
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["podio"].libs.directories[0])
        env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        if self.spec.satisfies("+sio @0.17:"):
            # sio needs to be on LD_LIBRARY_PATH for ROOT to be able to
            # dynamicaly load the python libraries also in dependent build
            # environments since the import structure has changed with
            # podio@0.17
            env.prepend_path("LD_LIBRARY_PATH", self.spec["sio"].libs.directories[0])

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
