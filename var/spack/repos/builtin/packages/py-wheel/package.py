# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWheel(Package, PythonExtension):
    """A built-package format for Python."""

    homepage = "https://github.com/pypa/wheel"
    url = "https://files.pythonhosted.org/packages/py3/w/wheel/wheel-0.41.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/wheel/"

    version(
        "0.43.0",
        sha256="55c570405f142630c6b9f72fe09d9b67cf1477fcf543ae5b8dcb1f5b7377da81",
        url="https://pypi.org/packages/7d/cd/d7460c9a869b16c3dd4e1e403cce337df165368c71d6af229a74699622ce/wheel-0.43.0-py3-none-any.whl",
    )
    version(
        "0.42.0",
        sha256="177f9c9b0d45c47873b619f5b650346d632cdc35fb5e4d25058e09c9e581433d",
        url="https://pypi.org/packages/c7/c3/55076fc728723ef927521abaa1955213d094933dc36d4a2008d5101e1af5/wheel-0.42.0-py3-none-any.whl",
    )
    version(
        "0.41.3",
        sha256="488609bc63a29322326e05560731bf7bfea8e48ad646e1f5e40d366607de0942",
        url="https://pypi.org/packages/fa/7f/4c07234086edbce4a0a446209dc0cb08a19bb206a3ea53b2f56a403f983b/wheel-0.41.3-py3-none-any.whl",
    )
    version(
        "0.41.2",
        sha256="75909db2664838d015e3d9139004ee16711748a52c8f336b52882266540215d8",
        url="https://pypi.org/packages/b8/8b/31273bf66016be6ad22bb7345c37ff350276cfd46e389a0c2ac5da9d9073/wheel-0.41.2-py3-none-any.whl",
    )
    version(
        "0.41.1",
        sha256="473219bd4cbedc62cea0cb309089b593e47c15c4a2531015f94e4e3b9a0f6981",
        url="https://pypi.org/packages/28/f5/6955d7b3a5d71ce6bac104f9cf98c1b0513ad656cdaca8ea7d579196f771/wheel-0.41.1-py3-none-any.whl",
    )
    version(
        "0.41.0",
        sha256="7e9be3bbd0078f6147d82ed9ed957e323e7708f57e134743d2edef3a7b7972a9",
        url="https://pypi.org/packages/17/11/f139e25018ea2218aeedbedcf85cd0dd8abeed29a38ac1fda7f5a8889382/wheel-0.41.0-py3-none-any.whl",
    )
    version(
        "0.40.0",
        sha256="d236b20e7cb522daf2390fa84c55eea81c5c30190f90f29ae2ca1ad8355bf247",
        url="https://pypi.org/packages/61/86/cc8d1ff2ca31a312a25a708c891cf9facbad4eae493b3872638db6785eb5/wheel-0.40.0-py3-none-any.whl",
    )
    version(
        "0.38.4",
        sha256="b60533f3f5d530e971d6737ca6d58681ee434818fab630c83a734bb10c083ce8",
        url="https://pypi.org/packages/bd/7c/d38a0b30ce22fc26ed7dbc087c6d00851fb3395e9d0dac40bec1f905030c/wheel-0.38.4-py3-none-any.whl",
    )
    version(
        "0.38.3",
        sha256="f3c99240da8d26989dca2d67a7a431015eb91fb301eecacc6e452133689d9d59",
        url="https://pypi.org/packages/3b/48/7a4e6e610cfbc71d727ac58ddc9abe0daf5772b81d5630a4aef9e919ad46/wheel-0.38.3-py3-none-any.whl",
    )
    version(
        "0.38.2",
        sha256="7a5a3095dceca97a3cac869b8fef4e89b83fafde21b6688f47b6fda7600eb441",
        url="https://pypi.org/packages/46/3a/73fcaf6487aa9a9b02ee9df30a24bdc2c1f0292fe559811936d67a9053c1/wheel-0.38.2-py3-none-any.whl",
    )
    version(
        "0.35.1",
        sha256="497add53525d16c173c2c1c733b8f655510e909ea78cc0e29d374243544b77a2",
        url="https://pypi.org/packages/a7/00/3df031b3ecd5444d572141321537080b40c1c25e1caa3d86cdd12e5e919c/wheel-0.35.1-py2.py3-none-any.whl",
    )

    extends("python")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/w/wheel/wheel-{1}-{0}-none-any.whl"
        if version >= Version("0.38"):
            python = "py3"
        else:
            python = "py2.py3"
        return url.format(python, version)

    def install(self, spec, prefix):
        # To build wheel from source, you need setuptools and wheel already installed.
        # We get around this by using a pre-built wheel, see:
        # https://discuss.python.org/t/bootstrapping-a-specific-version-of-pip/12306
        args = std_pip_args + ["--prefix=" + prefix, self.stage.archive_file]
        pip(*args)
