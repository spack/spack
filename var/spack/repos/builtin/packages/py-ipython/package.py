# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIpython(PythonPackage):
    """IPython provides a rich toolkit to help you make the most out of using
    Python interactively."""

    homepage = "https://ipython.readthedocs.org/"
    pypi = "ipython/ipython-7.18.1.tar.gz"
    git = "https://github.com/ipython/ipython"

    # "IPython.kernel" was deprecated for py-ipython@:7 and fails to import, leave
    # out of "import_modules" to ensure that import tests pass.
    # for py-ipython@8: "IPython.kernel" was removed
    skip_modules = ["IPython.kernel"]

    version("8.5.0", sha256="097bdf5cd87576fd066179c9f7f208004f7a6864ee1b20f37d346c0bcb099f84")
    version("8.0.1", sha256="ab564d4521ea8ceaac26c3a2c6e5ddbca15c8848fd5a5cc325f960da88d42974")
    version("7.31.1", sha256="b5548ec5329a4bcf054a5deed5099b0f9622eb9ea51aaa7104d215fece201d8c")
    version("7.28.0", sha256="2097be5c814d1b974aea57673176a924c4c8c9583890e7a5f082f547b9975b11")
    version("7.27.0", sha256="58b55ebfdfa260dad10d509702dc2857cb25ad82609506b070cf2d7b7df5af13")
    version("7.26.0", sha256="0cff04bb042800129348701f7bd68a430a844e8fb193979c08f6c99f28bb735e")
    version("7.21.0", sha256="04323f72d5b85b606330b6d7e2dc8d2683ad46c3905e955aa96ecc7a99388e70")
    version("7.18.1", sha256="a331e78086001931de9424940699691ad49dfb457cea31f5471eae7b78222d5e")
    version("7.5.0", sha256="e840810029224b56cd0d9e7719dc3b39cf84d577f8ac686547c8ba7a06eeab26")
    version("7.3.0", sha256="06de667a9e406924f97781bda22d5d76bfb39762b678762d86a466e63f65dc39")
    version("5.8.0", sha256="4bac649857611baaaf76bc82c173aa542f7486446c335fe1a6c05d0d491c8906")
    version("5.1.0", sha256="7ef4694e1345913182126b219aaa4a0047e191af414256da6772cf249571b961")
    version(
        "3.1.0",
        sha256="532092d3f06f82b1d8d1e5c37097eae19fcf025f8f6a4b670dd49c3c338d5624",
        deprecated=True,
    )
    version(
        "2.3.1",
        sha256="3e98466aa2fe54540bcba9aa6e01a39f40110d67668c297340c4b9514b7cc49c",
        deprecated=True,
    )

    depends_on("python@3.8:", when="@8:", type=("build", "run"))
    depends_on("python@3.7:", when="@7.17:", type=("build", "run"))
    depends_on("python@3.6:", when="@7.10:", type=("build", "run"))
    depends_on("python@3.5:", when="@7:", type=("build", "run"))
    depends_on("python@3.3:", when="@6:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools@51:", when="@8:", type="build")
    depends_on("py-setuptools@18.5:", when="@4.1:7", type="run")
    depends_on("py-setuptools", type="build")

    depends_on("py-appnope", when="@4: platform=darwin", type=("build", "run"))
    depends_on("py-backcall", when="@7.3.0:", type=("build", "run"))
    depends_on("py-colorama", when="@5: platform=windows", type=("build", "run"))
    depends_on("py-decorator", when="@4:", type=("build", "run"))
    depends_on("py-jedi@0.16:", when="@7.18,7.20:", type=("build", "run"))
    depends_on("py-jedi@0.10:", when="@7.5:7.17,7.19", type=("build", "run"))
    depends_on("py-matplotlib-inline", when="@7.23:", type=("build", "run"))
    depends_on("py-pexpect@4.4:", when="@7.18: platform=linux", type=("build", "run"))
    depends_on("py-pexpect@4.4:", when="@7.18: platform=darwin", type=("build", "run"))
    depends_on("py-pexpect@4.4:", when="@7.18: platform=cray", type=("build", "run"))
    depends_on("py-pexpect", when="@4: platform=linux", type=("build", "run"))
    depends_on("py-pexpect", when="@4: platform=darwin", type=("build", "run"))
    depends_on("py-pexpect", when="@4: platform=cray", type=("build", "run"))
    depends_on("py-pickleshare", when="@4:", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.2:3.0", when="@8.5:", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2,3.0.2:3.0", when="@7.26:", type=("build", "run"))
    depends_on("py-prompt-toolkit@3.0.2:3.0", when="@7.18:7.25", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2.0", when="@7.5.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@2.0.0:2", when="@7.0.0:7.5.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@1.0.4:1", when="@5:7.0.0", type=("build", "run"))
    depends_on("py-prompt-toolkit@1.0.3:1", when="@5:7.0.0", type=("build", "run"))
    depends_on("py-pygments@2.4:", when="@8.1:", type=("build", "run"))
    depends_on("py-pygments", when="@5:", type=("build", "run"))
    depends_on("py-stack-data", when="@8:", type=("build", "run"))
    depends_on("py-traitlets@5:", when="@8:", type=("build", "run"))
    depends_on("py-traitlets@4.2:", when="@5:", type=("build", "run"))
    depends_on("py-traitlets", when="@4:", type=("build", "run"))

    depends_on("py-black", when="@8.0", type=("build", "run"))
    depends_on("py-simplegeneric@0.8:", when="@4:7.0.0", type=("build", "run"))
