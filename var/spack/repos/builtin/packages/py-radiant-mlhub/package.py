# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadiantMlhub(PythonPackage):
    """A Python client for Radiant MLHub."""

    homepage = "https://github.com/radiantearth/radiant-mlhub"
    pypi = "radiant-mlhub/radiant_mlhub-0.2.1.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "0.5.5",
        sha256="f5d1785da5357db55261f593c097fbd5a93c6be5f7167c1388ff5eb6d04db539",
        url="https://pypi.org/packages/98/99/00a8ebc4784a9237bf058f723fbe9ffca60f9b457cc58bb289cf076175b1/radiant_mlhub-0.5.5-py3-none-any.whl",
    )
    version(
        "0.5.3",
        sha256="846c3b9b9409059699be2420478c1ba251c5f2e626a470e78c89de7d73832442",
        url="https://pypi.org/packages/95/d9/4b76f01acfe0b363d5f8285c054ee044b0d28965b6032d8689ddc4012a87/radiant_mlhub-0.5.3-py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="5f875e3e377122c1607ce70e1fb5c30ad04537b9c68f66ad71f1113b66c1ebdd",
        url="https://pypi.org/packages/91/7d/d73ef337836e1d515c5c49cc1efb3b5c3091e7eaca4906a7218262bf7ae3/radiant_mlhub-0.5.2-py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="a77fbccda2c55de68b1b8c39e75b925ba537dd6a28acfc46011613eb34ee91fd",
        url="https://pypi.org/packages/55/ae/7b5654b9634fea6bd88e265e67c3d7071d6d79a75e742b9557208010e483/radiant_mlhub-0.5.1-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="78d44487080ce25567809579d315dd780ae038a2a2b1843a692447b3c8d21481",
        url="https://pypi.org/packages/02/03/82e1208930c0f6397c5305de6363daee50f227a931874232106d5e434e81/radiant_mlhub-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.1",
        sha256="755b9556f10e1ec0da433e35ab5b1d6a0f7bfcf5d6ebe630114e0ffaa3861a4b",
        url="https://pypi.org/packages/c2/f6/bc1f6c62f1ad0627240de897d856916892e967d20cb90bf3c90658091112/radiant_mlhub-0.4.1-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="d88fd49b51290bb03f51362f17da4a698aa7b13454262508658271bcadd6c009",
        url="https://pypi.org/packages/fc/68/66d8f488d52b94dbef25b54d7b048e195fca51c3ad031ad8a9a95d698731/radiant_mlhub-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="706197a43e07a341015fdcad420cf17a452d48baa4ebd56bc9855becf2c52150",
        url="https://pypi.org/packages/e6/b3/b16fc24799defc9bcf1394b757c2b0e3f02eb79f40ae70a4bcbf33483296/radiant_mlhub-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="7edf56381fa8e48fb992ec042635f29bc468bed0e51ba60520ae2bb3c2180e2b",
        url="https://pypi.org/packages/7a/ae/e34beb7d4da6b6cf7e4000dda93157a40504287af29e11dce0402164db49/radiant_mlhub-0.3.0-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="fe3bf4d66e26b8b7071f9fa1d2196a8b894312b4244f16389f02d027fd0cac99",
        url="https://pypi.org/packages/da/7b/6f515a5a114e0732acf008f185b6ffe1f895ede0eb674de134f35a5a2dc0/radiant_mlhub-0.2.2-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="02d9b56cdddee25665fc650abead516789709ebbc1837d77c69edfd2493b093f",
        url="https://pypi.org/packages/d0/9d/7e226b0bd483260fa309d10bc6cb68ffbd965825d795055e3a4dd002635b/radiant_mlhub-0.2.1-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="cbb68a0d0ea56bd0999c4112627448dc3543c0ffeda035e6743c4f1439d2531a",
        url="https://pypi.org/packages/75/d4/7e7fadd4a519c43977fb6d4026fc0d130db3fc05fbbc4a7167105aa75636/radiant_mlhub-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.5:")
        depends_on("python@3.7:", when="@0.3:0.4")
        depends_on("py-click@7.1.2:", when="@0.3:")
        depends_on("py-click@7.1.2:7", when="@0.1:0.2")
        depends_on("py-pydantic@1.9.2:1.9", when="@0.5.2:")
        depends_on("py-pydantic@1.9.0:1", when="@0.5:0.5.1")
        depends_on("py-pystac@1.4", when="@0.5.2:")
        depends_on("py-pystac@1.4:", when="@0.5:0.5.1")
        depends_on("py-pystac@1.1:", when="@0.3:0.4")
        depends_on("py-pystac@0.5.4", when="@0.2")
        depends_on("py-python-dateutil@2.8.2:2.8", when="@0.5.2:")
        depends_on("py-python-dateutil@2.8:", when="@0.5:0.5.1")
        depends_on("py-requests@2.27", when="@0.5.2:")
        depends_on("py-requests@2.27:", when="@0.5:0.5.1")
        depends_on("py-requests@2.25:", when="@0.3:0.4")
        depends_on("py-requests@2.25.1:2.25", when="@0.1:0.2")
        depends_on("py-shapely@1.8.0:1", when="@0.5:")
        depends_on("py-tqdm@4.64", when="@0.5.2:")
        depends_on("py-tqdm@4.64:", when="@0.5:0.5.1")
        depends_on("py-tqdm@4.56:", when="@0.3:0.4")
        depends_on("py-tqdm@4.56", when="@0.1:0.2")
        depends_on("py-typing-extensions@3.7:", when="@0.4.1:0.4 ^python@:3.7")
        depends_on("py-urllib3@1.26.11:1", when="@0.5.5:")

    # Historical dependencies
