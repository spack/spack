# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptools(Package, PythonExtension):
    """A Python utility that aids in the process of downloading, building,
    upgrading, installing, and uninstalling Python packages."""

    homepage = "https://github.com/pypa/setuptools"
    url = "https://files.pythonhosted.org/packages/py3/s/setuptools/setuptools-62.3.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/setuptools/"

    version(
        "67.6.0",
        sha256="b78aaa36f6b90a074c1fa651168723acbf45d14cb1196b6f02c0fd07f17623b2",
        expand=False,
    )
    version(
        "65.5.0",
        sha256="f62ea9da9ed6289bfe868cd6845968a2c854d1427f8548d52cae02a42b4f0356",
        expand=False,
    )
    version(
        "65.0.0",
        sha256="fe9a97f68b064a6ddd4bacfb0b4b93a4c65a556d97ce906255540439d0c35cef",
        expand=False,
    )
    version(
        "64.0.0",
        sha256="63f463b90ff5e0a1422010100268fd688e15c44ae0798659013c8412963e15e4",
        expand=False,
    )
    version(
        "63.4.3",
        sha256="7f61f7e82647f77d4118eeaf43d64cbcd4d87e38af9611694d4866eb070cd10d",
        expand=False,
    )
    version(
        "63.0.0",
        sha256="045aec56a3eee5c82373a70e02db8b6da9a10f7faf61ff89a14ab66c738ed370",
        expand=False,
    )
    version(
        "62.6.0",
        sha256="c1848f654aea2e3526d17fc3ce6aeaa5e7e24e66e645b5be2171f3f6b4e5a178",
        expand=False,
    )
    version(
        "62.4.0",
        sha256="5a844ad6e190dccc67d6d7411d119c5152ce01f7c76be4d8a1eaa314501bba77",
        expand=False,
    )
    version(
        "62.3.2",
        sha256="68e45d17c9281ba25dc0104eadd2647172b3472d9e01f911efa57965e8d51a36",
        expand=False,
    )
    version(
        "59.4.0",
        sha256="feb5ff19b354cde9efd2344ef6d5e79880ce4be643037641b49508bbb850d060",
        expand=False,
    )
    version(
        "58.2.0",
        sha256="2551203ae6955b9876741a26ab3e767bb3242dafe86a32a749ea0d78b6792f11",
        expand=False,
    )
    version(
        "57.4.0",
        sha256="a49230977aa6cfb9d933614d2f7b79036e9945c4cdd7583163f4e920b83418d6",
        expand=False,
    )
    version(
        "57.1.0",
        sha256="ddae4c1b9220daf1e32ba9d4e3714df6019c5b583755559be84ff8199f7e1fe3",
        expand=False,
    )
    version(
        "51.0.0",
        sha256="8c177936215945c9a37ef809ada0fab365191952f7a123618432bbfac353c529",
        expand=False,
    )
    version(
        "50.3.2",
        sha256="2c242a0856fbad7efbe560df4a7add9324f340cf48df43651e9604924466794a",
        expand=False,
    )
    version(
        "50.1.0",
        sha256="4537c77e6e7dc170081f8547564551d4ff4e4999717434e1257600bbd3a23296",
        expand=False,
    )
    version(
        "49.6.0",
        sha256="4dd5bb0a0a0cff77b46ca5dd3a84857ee48c83e8223886b556613c724994073f",
        expand=False,
    )
    version(
        "49.2.0",
        sha256="272c7f48f5cddc5af5901f4265274c421c7eede5c8bc454ac2903d3f8fc365e9",
        expand=False,
    )
    version(
        "46.1.3",
        sha256="4fe404eec2738c20ab5841fa2d791902d2a645f32318a7850ef26f8d7215a8ee",
        expand=False,
    )
    version(
        "44.1.1",
        sha256="27a714c09253134e60a6fa68130f78c7037e5562c4f21f8f318f2ae900d152d5",
        expand=False,
    )
    version(
        "44.1.0",
        sha256="992728077ca19db6598072414fb83e0a284aca1253aaf2e24bb1e55ee6db1a30",
        expand=False,
    )
    version(
        "43.0.0",
        sha256="a67faa51519ef28cd8261aff0e221b6e4c370f8fb8bada8aa3e7ad8945199963",
        expand=False,
    )
    version(
        "41.4.0",
        sha256="8d01f7ee4191d9fdcd9cc5796f75199deccb25b154eba82d44d6a042cf873670",
        expand=False,
    )
    version(
        "41.3.0",
        sha256="e9832acd9be6f3174f4c34b40e7d913a146727920cbef6465c1c1bd2d21a4ec4",
        expand=False,
    )
    version(
        "41.0.1",
        sha256="c7769ce668c7a333d84e17fe8b524b1c45e7ee9f7908ad0a73e1eda7e6a5aebf",
        expand=False,
    )
    version(
        "41.0.0",
        sha256="e67486071cd5cdeba783bd0b64f5f30784ff855b35071c8670551fd7fc52d4a1",
        expand=False,
    )
    version(
        "40.8.0",
        sha256="e8496c0079f3ac30052ffe69b679bd876c5265686127a3159cfa415669b7f9ab",
        expand=False,
    )
    version(
        "40.4.3",
        sha256="ce4137d58b444bac11a31d4e0c1805c69d89e8ed4e91fde1999674ecc2f6f9ff",
        expand=False,
    )
    version(
        "40.2.0",
        sha256="ea3796a48a207b46ea36a9d26de4d0cc87c953a683a7b314ea65d666930ea8e6",
        expand=False,
    )
    version(
        "39.2.0",
        sha256="8fca9275c89964f13da985c3656cb00ba029d7f3916b37990927ffdf264e7926",
        expand=False,
    )
    version(
        "39.0.1",
        sha256="8010754433e3211b9cdbbf784b50f30e80bf40fc6b05eb5f865fab83300599b8",
        expand=False,
    )
    version(
        "25.2.0",
        sha256="2845247c359bb91097ccf8f6be8a69edfa44847f3d2d5def39aa43c3d7f615ca",
        expand=False,
    )
    version(
        "20.7.0",
        sha256="8917a52aa3a389893221b173a89dae0471022d32bff3ebc31a1072988aa8039d",
        expand=False,
    )
    version(
        "20.6.7",
        sha256="9982ee4d279a2541dc1a7efee994ff9c535cfc05315e121e09df7f93da48c442",
        expand=False,
    )

    extends("python")
    depends_on("python@3.7:", when="@59.7:", type=("build", "run"))
    depends_on("python@3.6:", when="@51:", type=("build", "run"))
    depends_on("python@3.5:", when="@45:50", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@44", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", when="@:43", type=("build", "run"))
    depends_on("py-pip", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/s/setuptools/setuptools-{1}-{0}-none-any.whl"

        if version >= Version("45.1.0"):
            python_tag = "py3"
        else:
            python_tag = "py2.py3"
        return url.format(python_tag, version)

    def install(self, spec, prefix):
        # When setuptools changes its entry point we might get weird
        # incompatibilities if building from sources in a non-isolated environment.
        #
        # https://github.com/pypa/setuptools/issues/980#issuecomment-1154471423
        #
        # We work around this issue by installing setuptools from wheels
        whl = self.stage.archive_file
        args = ["-m", "pip"] + std_pip_args + ["--prefix=" + prefix, whl]
        python(*args)
