# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    license("BSD-3-Clause")

    version(
        "8.14.0",
        sha256="248aca623f5c99a6635bc3857677b7320b9b8039f99f070ee0d20a5ca5a8e6bf",
        url="https://pypi.org/packages/52/d1/f70cdafba20030cbc1412d7a7d6a89c5035071835cc50e47fc5ed8da553c/ipython-8.14.0-py3-none-any.whl",
    )
    version(
        "8.11.0",
        sha256="5b54478e459155a326bf5f42ee4f29df76258c0279c36f21d71ddb560f88b156",
        url="https://pypi.org/packages/ac/91/23e08c442657cf493598b0222008437c9e0aef0709a8fd65a5d5d68ffa21/ipython-8.11.0-py3-none-any.whl",
    )
    version(
        "8.5.0",
        sha256="6f090e29ab8ef8643e521763a4f1f39dc3914db643122b1e9d3328ff2e43ada2",
        url="https://pypi.org/packages/13/0d/ad3266203acb01189588aac9c1fc4dc982b58b0512ddb3cd4bea3cc26e22/ipython-8.5.0-py3-none-any.whl",
    )
    version(
        "8.0.1",
        sha256="c503a0dd6ccac9c8c260b211f2dd4479c042b49636b097cc9a0d55fe62dff64c",
        url="https://pypi.org/packages/ef/88/3e505ba3accd31f464f92dcd8c229f2d0d7af14ead91c1899c52648336be/ipython-8.0.1-py3-none-any.whl",
    )
    version(
        "7.31.1",
        sha256="55df3e0bd0f94e715abd968bedd89d4e8a7bce4bf498fb123fed4f5398fea874",
        url="https://pypi.org/packages/b8/b4/4d6c2753effd9c4e0d93fad9a3827760eaecec8331fe550f5d49e22cce89/ipython-7.31.1-py3-none-any.whl",
    )
    version(
        "7.28.0",
        sha256="f16148f9163e1e526f1008d7c8d966d9c15600ca20d1a754287cf96d00ba6f1d",
        url="https://pypi.org/packages/76/d1/e6166fc278a0aab9c2997ae241346837368fc9aa0c6eea9b0dbe2d727004/ipython-7.28.0-py3-none-any.whl",
    )
    version(
        "7.27.0",
        sha256="75b5e060a3417cf64f138e0bb78e58512742c57dc29db5a5058a2b1f0c10df02",
        url="https://pypi.org/packages/50/b1/618daafee1bbc6e7e9dceb105eca919ca8eceeeda8b80282e25d416df39b/ipython-7.27.0-py3-none-any.whl",
    )
    version(
        "7.26.0",
        sha256="892743b65c21ed72b806a3a602cca408520b3200b89d1924f4b3d2cdb3692362",
        url="https://pypi.org/packages/25/a0/e0b850415984ac29f14775b075efc54d73b38f0d50c6ebdea7820ffb1c12/ipython-7.26.0-py3-none-any.whl",
    )
    version(
        "7.21.0",
        sha256="34207ffb2f653bced2bc8e3756c1db86e7d93e44ed049daae9814fed66d408ec",
        url="https://pypi.org/packages/3b/43/6dbd0610550708fc418ad027fda97b5f415da9053749641654fdacfec93f/ipython-7.21.0-py3-none-any.whl",
    )
    version(
        "7.18.1",
        sha256="2e22c1f74477b5106a6fb301c342ab8c64bb75d702e350f05a649e8cb40a0fb8",
        url="https://pypi.org/packages/72/36/89e1bb437f4f2275c33acc6eb333ab2d1c64e732ad23d6f34825b512e1a3/ipython-7.18.1-py3-none-any.whl",
    )
    version(
        "7.5.0",
        sha256="54c5a8aa1eadd269ac210b96923688ccf01ebb2d0f21c18c3c717909583579a8",
        url="https://pypi.org/packages/a9/2e/41dce4ed129057e05a555a7f9629aa2d5f81fdcd4d16568bc24b75a1d2c9/ipython-7.5.0-py3-none-any.whl",
    )
    version(
        "7.3.0",
        sha256="5d3e020a6b5f29df037555e5c45ab1088d6a7cf3bd84f47e0ba501eeb0c3ec82",
        url="https://pypi.org/packages/14/3b/3fcf422a99a04ee493e6a4fc3014e3c8ff484a7feed238fef68bdc285085/ipython-7.3.0-py3-none-any.whl",
    )
    version(
        "5.8.0",
        sha256="0371b7e4bd74954a35086eac949beeac5b1c9f5ce231e2e77df2286a293765e3",
        url="https://pypi.org/packages/3c/01/72cfbf8d195f98cff18e7b160c5c3b5e3fb71ad7be08e630f6ba0793c561/ipython-5.8.0-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="4452b99ed28453c68dbd2765899d3df8fa5b2bb98dcceb2028ca9c0ccbcc37eb",
        url="https://pypi.org/packages/66/d3/8830812574574c39f97bd6390475ba76294ed70cf489995dd30bd9b38245/ipython-5.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@8.13.1:8.18")
        depends_on("python@3.8:", when="@8:8.13.0")
        depends_on("python@3.7:", when="@7.17:7")
        depends_on("py-appnope", when="@:8.17 platform=darwin")
        depends_on("py-backcall", when="@6.3:8.16")
        depends_on("py-black", when="@8:8.0")
        depends_on("py-colorama", when="@5: platform=windows")
        depends_on("py-decorator")
        depends_on("py-jedi@0.16:", when="@7.18:7.18.0,7.20:")
        depends_on("py-jedi@0.10:", when="@6:7.16.1,7.17,7.18.1:7.19")
        depends_on("py-matplotlib-inline", when="@7.23:")
        depends_on("py-pexpect@4.3.1:", when="@7.18: platform=linux")
        depends_on("py-pexpect@4.3.1:", when="@7.18: platform=freebsd")
        depends_on("py-pexpect@4.3.1:", when="@7.18: platform=darwin")
        depends_on("py-pexpect@4.3.1:", when="@7.18: platform=cray")
        depends_on("py-pexpect", when="@:7.17 platform=linux")
        depends_on("py-pexpect", when="@:7.17 platform=freebsd")
        depends_on("py-pexpect", when="@:7.17 platform=darwin")
        depends_on("py-pexpect", when="@:7.17 platform=cray")
        depends_on("py-pickleshare", when="@:8.16")
        depends_on("py-prompt-toolkit@3.0.30:3.0.36,3.0.38:", when="@8.11:8.18.0")
        depends_on("py-prompt-toolkit@3.0.2:", when="@8.5:8.6")
        depends_on("py-prompt-toolkit@2,3.0.2:", when="@7.10.1:8.4")
        depends_on("py-prompt-toolkit@2", when="@7:7.9")
        depends_on("py-prompt-toolkit@1.0.4:1", when="@5.2:6.2")
        depends_on("py-prompt-toolkit@1.0.3:1", when="@5.0.0-rc1:5.1")
        depends_on("py-pygments@2.4:", when="@8.1:")
        depends_on("py-pygments", when="@5:5.9,6:8.0")
        depends_on("py-setuptools@18.5:", when="@:8.4")
        depends_on("py-simplegeneric@0.8.1:", when="@:7.0")
        depends_on("py-stack-data", when="@8:")
        depends_on("py-traitlets@5.0.0:", when="@8:8.22.0")
        depends_on("py-traitlets@4.2:", when="@5:7")
        depends_on("py-typing-extensions", when="@8.12: ^python@:3.9")
        depends_on("py-win-unicode-console@0.5:", when="@5.0.0-rc1:5.1 platform=windows")

    # Historical dependencies
