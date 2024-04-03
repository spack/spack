# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbformat(PythonPackage):
    """The Jupyter Notebook format"""

    homepage = "https://github.com/jupyter/nbformat"
    pypi = "nbformat/nbformat-5.0.7.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.8.0",
        sha256="d910082bd3e0bffcf07eabf3683ed7dda0727a326c446eeb2922abe102e65162",
        url="https://pypi.org/packages/1d/f6/38f4694b5035306a8c2685e9e6ea7bf46ea344c03422d7131442ac9677c1/nbformat-5.8.0-py3-none-any.whl",
    )
    version(
        "5.7.0",
        sha256="1b05ec2c552c2f1adc745f4eddce1eac8ca9ffd59bb9fd859e827eaa031319f9",
        url="https://pypi.org/packages/5c/9f/957655d02f43b8bff77e6da08c94472b1229c13e7455bbd662163c9b78c0/nbformat-5.7.0-py3-none-any.whl",
    )
    version(
        "5.4.0",
        sha256="0d6072aaec95dddc39735c144ee8bbc6589c383fb462e4058abc855348152dad",
        url="https://pypi.org/packages/2f/9a/97151abb954af0cc5d0e3ff2eb7b6d96704a317ac2c0ce0cc76cef003991/nbformat-5.4.0-py3-none-any.whl",
    )
    version(
        "5.1.3",
        sha256="eb8447edd7127d043361bc17f2f5a807626bc8e878c7709a1c647abda28a9171",
        url="https://pypi.org/packages/e7/c7/dd50978c637a7af8234909277c4e7ec1b71310c13fb3135f3c8f5b6e045f/nbformat-5.1.3-py3-none-any.whl",
    )
    version(
        "5.0.7",
        sha256="ea55c9b817855e2dfcd3f66d74857342612a60b1f09653440f4a5845e6e3523f",
        url="https://pypi.org/packages/4d/d1/b568bd35f95321f152f594b3647cd080e96d3347843ff2fa34dce871b8bf/nbformat-5.0.7-py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="b9a0dbdbd45bb034f4f8893cafd6f652ea08c8c1674ba83f2dc55d3955743b0b",
        url="https://pypi.org/packages/da/27/9a654d2b6cc1eaa517d1c5a4405166c7f6d72f04f6e7eea41855fe808a46/nbformat-4.4.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="02f3474203248214f7a34ad0955d75490462dc0e328f9920d1ea8aa795ae3399",
        url="https://pypi.org/packages/d6/4c/8058f1170dbdbe5a66e9431489f85d2d3e5a8e6314dd7ed1f7b10d864a70/nbformat-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="d304387f78d651edf3a3285052601aa8b7fe6d52dcd57e4ffd2869b2b65fda1c",
        url="https://pypi.org/packages/11/2d/83180bdaa7c8aa1ff2308b928607d66ae907fb7061cbe59dc1e6243b69db/nbformat-4.0.1-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="a4543847ce9b6676000812996757d816cb8cecc02ecc1a413c29c303a30bd208",
        url="https://pypi.org/packages/03/ac/befb692b03d880f9d66b9f09bf3277634480d7acad743511e83b88649085/nbformat-4.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.2:5.8")
        depends_on("py-fastjsonschema", when="@5.3:")
        depends_on("py-importlib-metadata@3.6:", when="@5.6.1:5.8 ^python@:3.7")
        depends_on("py-ipython-genutils", when="@4.1:5.1")
        depends_on("py-jsonschema@2.6:", when="@5.3:")
        depends_on("py-jsonschema@2.4,2.5.1:", when="@4.2:5.2")
        depends_on("py-jsonschema@2:2.4,2.5.1:", when="@4.1")
        depends_on("py-jupyter-core", when="@4.1:")
        depends_on("py-traitlets@5.1:", when="@5.4:")
        depends_on("py-traitlets@4.1.0:", when="@4.2:5.3")
        depends_on("py-traitlets", when="@4.1")

    # Historical dependencies
