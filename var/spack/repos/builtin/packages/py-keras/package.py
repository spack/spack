# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyKeras(PythonPackage):
    """Deep Learning for humans.

    Keras is a deep learning API written in Python, running on top of the machine
    learning platform TensorFlow. It was developed with a focus on enabling fast
    experimentation. Being able to go from idea to result as fast as possible is
    key to doing good research.
    """

    homepage = "https://keras.io"
    git = "https://github.com/keras-team/keras.git"
    url = "https://github.com/keras-team/keras/archive/refs/tags/v2.7.0.tar.gz"

    version("2.10.0", sha256="b1d8d9358700f4a585455854a142d88cc987419c1638ef935b440842d593ad04")
    version("2.9.0", sha256="90226eaa0337573304f3e5ab44d4d9e3a65fe002776c5cbd0f65b738152c1084")
    version("2.8.0", sha256="5e777b0101d8385d3a90fc9056f1b2f6313f2c830d2e8181828b300c9229ec0c")
    version("2.7.0", sha256="7502746467ab15184e2e267f13fbb2c3f33ba24f8e02a097d229ba376dabaa04")
    version("2.6.0", sha256="15586a3f3e1ed9182e6e0d4c0dbd052dfb7250e779ceb7e24f8839db5c63fcae")
    version("2.5.0", commit="9c266106163390f173625c4e7b1ccb03ae145ffc", deprecated=True)
    version("2.4.3", sha256="fedd729b52572fb108a98e3d97e1bac10a81d3917d2103cc20ab2a5f03beb973")
    version("2.4.2", sha256="e26bc51b7b8fb7add452cdf6fba77d6509e6c78b9d9ef5fd32fe132c6d9182d2")
    version("2.4.1", sha256="e282cc9c5c996043b21d045765c0c5bf541c1879232a97a574c51af0ce132cb1")
    version("2.4.0", sha256="e31c6d2910767ab72f630309286fb7bf5476810dd64fde3e254054478442e9b0")
    version("2.3.1", sha256="321d43772006a25a1d58eea17401ef2a34d388b588c9f7646c34796151ebc8cc")
    version("2.3.0", sha256="a0d6ecf1d71cd0b85ea1da27ea7314a9d4723f5b468b7cedd87dcad0a491b354")
    version("2.2.5", sha256="0fb448b95643a708d25d2394183a2f3a84eefb55fb64917152a46826990113ea")
    version("2.2.4", sha256="90b610a3dbbf6d257b20a079eba3fdf2eed2158f64066a7c6f7227023fd60bc9")
    version("2.2.3", sha256="694aee60a6f8e0d3d6d3e4967e063b4623e3ca90032f023fd6d16bb5f81d18de")
    version("2.2.2", sha256="468d98da104ec5c3dbb10c2ef6bb345ab154f6ca2d722d4c250ef4d6105de17a")
    version("2.2.1", sha256="0d3cb14260a3fa2f4a5c4c9efa72226ffac3b4c50135ba6edaf2b3d1d23b11ee")
    version("2.2.0", sha256="5b8499d157af217f1a5ee33589e774127ebc3e266c833c22cb5afbb0ed1734bf")
    version("2.1.6", sha256="c14af1081242c25617ade7eb62121d58d01f16e1e744bae9fc4f1f95a417716e")
    version("2.1.5", sha256="907ad29add1fff27342a9f4fe3e60003d450d3af41a38f22f629c7736fc8399d")
    version("2.1.4", sha256="7ee1fcc79072ac904a4f008d715bcb78c60250ae3cd41d99e268c60ade8d0d3a")
    version("2.1.3", sha256="7ca3a381523bad40a6922e88951a316664cb088fd01cea07e5ec8ada3327e3c7")
    version("2.1.2", sha256="3ee56fc129d9d00b1916046e50056047836f97ada59df029e5661fb34442d5e8")
    version("2.1.1", sha256="f0ca2458c60d9711edf4291230b31795307ad3781cb6232ff4792b53c8f55123")
    version("2.1.0", sha256="67a0d66c20fff99312fc280e34c8f6dc3dbb027d4a33c13c79bec3c1173f6909")
    version("2.0.9", sha256="6b8572cf1b4a22fd0120b7c23382ba4fa04a6f0397e02af1249be9a7309d1767")
    version("2.0.8", sha256="899dc6aaed366f20100b9f80cf1093ea5b43eecc74afd1dc63a4e48dfa776ab9")
    version("2.0.7", sha256="a6c72ee2b94be1ffefe7e77b69582b9827211f0c356b2189459711844d3634c0")
    version("2.0.6", sha256="0519480abe4ad18b2c2d1bc580eab75edd82c95083d341a1157952f4b00019bb")
    version("2.0.5", sha256="cbce24758530e070fe1b403d6d21391cbea78c037b70bf6afc1ca9f1f8269eff")
    version("2.0.4", sha256="1cbe62af6821963321b275d5598fd94e63c11feaa1d4deaa79c9eb9ee0e1d68a")
    version("2.0.3", sha256="398dbd4a95e9d3ab2b2941d3e0c19362d397a2a6c3a667ab89d3d6aad30997f4")
    version("2.0.2", sha256="53fd0a6e9eaca2563e13d2266eac2da478fa25092de3c665aa26e380a8126841")
    version("2.0.1", sha256="c5c2727518f76606794363c01430f4992e482b4ab0dc6a8fa137c896855c09a8")
    version("2.0.0", sha256="02846dceb36e98368f47ca090d0f5fe6828e22ece10668a07047bea4c92b157f")
    version("1.2.2", sha256="d2b18c4336eb9c4f0d03469870257efa7980a9b036c9d46dcf4d49e7f4487e2d")
    version("1.2.1", sha256="6adce75b2050608e6683c3046ef938bfdc5bfcd4c6b6c522df5e50d18e0ac7c6")
    version("1.2.0", sha256="33d5297cd0c280640dc5c075466995c05911bc1da35c83ae57b2a48188b605e2")
    version("1.1.2", sha256="cfde0a424961ead4982a7ebefd77d8ca382810b5a69b566fa64c57d8f340eeb4")
    version("1.1.1", sha256="be1b67f62e5119f6f24a239a865dc47e6d9aa93b97b506ba34cab7353dbc23b6")
    version("1.1.0", sha256="36d83b027ba9d2c9da8e1eefc28f600ca93dc03423e033b633cbac9061af8a5d")

    # Supported Python versions listed in multiple places:
    # * keras/tools/pip_package/setup.py
    # * CONTRIBUTING.md
    # * PKG-INFO
    depends_on("python@3.7:", type=("build", "run"), when="@2.7:")
    depends_on("python@3.6:", type=("build", "run"), when="@2.4:")
    depends_on("py-setuptools", type="build")

    # Required dependencies listed in multiple places:
    # * BUILD
    # * WORKSPACE
    # * requirements.txt
    # * setup.py
    depends_on("pil", type=("build", "run"))
    depends_on("py-absl-py", type=("build", "run"), when="@2.6:")
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy@1.21.4:1.21", type=("build", "run"), when="@2.8:")
    depends_on("py-numpy@1.19.2:1.19", type=("build", "run"), when="@2.7")
    depends_on("py-numpy@1.9.1:", type=("build", "run"), when="@2.0.8:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"), when="@2.0.9:")
    depends_on("py-pydot", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scipy@1.5.2:1.5", type=("build", "run"), when="@2.6:")
    depends_on("py-scipy@0.14:", type=("build", "run"), when="@2.0.8:")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    for minor_ver in range(5, 11):
        depends_on(
            "py-tensorflow@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )
        depends_on(
            "py-tensorboard@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )
    depends_on("py-theano", type=("build", "run"), when="@:2.0.7")

    # Required dependencies not listed anywhere?
    depends_on("bazel", type="build", when="@2.5:")
    depends_on("protobuf", type="build", when="@2.5:")

    def url_for_version(self, version):
        if version >= Version("2.6"):
            return super(PyKeras, self).url_for_version(version)
        else:
            url = "https://pypi.io/packages/source/K/Keras/Keras-{0}.tar.gz"
            return url.format(version.dotted)

    @when("@2.5:")
    def patch(self):
        infile = join_path(self.package_dir, "protobuf_build.patch")
        with open(infile, "r") as source_file:
            text = source_file.read()
        with open("keras/keras.bzl", mode="a") as f:
            f.write(text)

        filter_file(
            'load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")',
            'load("@org_keras//keras:keras.bzl", "py_proto_library")',
            "keras/protobuf/BUILD",
            string=True,
        )

    @when("@2.5:")
    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["HOME"] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + self.tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            # Show (formatted) subcommands being executed
            "--subcommands=pretty_print",
            "--spawn_strategy=local",
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            "--explain=explainlogfile.txt",
            # Increase verbosity of explanation,
            "--verbose_explanations",
            # bazel uses system PYTHONPATH instead of spack paths
            "--action_env",
            "PYTHONPATH={0}".format(env["PYTHONPATH"]),
            "//keras/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable("bazel-bin/keras/tools/pip_package/build_pip_package")
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)

        with working_dir(buildpath):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)
        remove_linked_tree(self.tmp_path)
