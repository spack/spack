# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClickOptionGroup(PythonPackage):
    """click-option-group is a Click-extension package that adds option groups missing in Click."""

    homepage = "https://github.com/click-contrib/click-option-group/"

    pypi = "click-option-group/click-option-group-0.5.6.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.5.6",
        sha256="38a26d963ee3ad93332ddf782f9259c5bdfe405e73408d943ef5e7d0c3767ec7",
        url="https://pypi.org/packages/af/75/81ea958bc0f7e410257cb2a42531b93a7695a31930cde87192c010a52c50/click_option_group-0.5.6-py3-none-any.whl",
    )
    version(
        "0.5.5",
        sha256="0f8ca79bc9b1d6fcaafdbe194b17ba1a2dde44ddf19087235c3efed2ad288143",
        url="https://pypi.org/packages/cf/b2/808e028b944a1f7c21005205762ee88654c40b73b9de2a04e18384d1c9cd/click_option_group-0.5.5-py3-none-any.whl",
    )
    version(
        "0.5.4",
        sha256="0976f0dd15ab5f9f2ee0823f4b83c5a84f8748668c0c37a334739b287711940d",
        url="https://pypi.org/packages/36/84/06316d5fc1c5fa011b293effae02303bc616d5a7c93d4c68e88c027124fc/click_option_group-0.5.4-py3-none-any.whl",
    )
    version(
        "0.5.3",
        sha256="9653a2297357335d7325a1827e71ac1245d91c97d959346a7decabd4a52d5354",
        url="https://pypi.org/packages/6f/87/88c4909488caca67c0fe435912efa7904955e6f36fc73106d56334252a94/click_option_group-0.5.3-py3-none-any.whl",
    )
    version(
        "0.5.2",
        sha256="1b4b2ecf87ba8dea78060cffd294b38eea5af81f28a5f9be223c01b8c5ea9ab0",
        url="https://pypi.org/packages/8a/28/8c81b5b7ef0b831dac1bc23f807e264a38b3bcfb1280f7cf5dedf18b6651/click_option_group-0.5.2-py3-none-any.whl",
    )
    version(
        "0.5.1",
        sha256="b363552b81f3bc9bef2402837b08865d186bd97c2311768f7d52aaf896e384a6",
        url="https://pypi.org/packages/30/e9/1b3d4e54586f350c39f1d2077c5dfd3bc42138b5b80ded4a62462442064c/click_option_group-0.5.1-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="e5bdea3ffa7009104e14bcce43feb46ae5b0132d7b9a167641566830e2c289bc",
        url="https://pypi.org/packages/bc/f0/7e670df7f9c8e492e3af08fbfeedb6687b50c67205de70b1e417a199e35c/click_option_group-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="6f1efaf1c587590eff849adbe1f633c4402598eafe0082d364479cba732003cf",
        url="https://pypi.org/packages/67/79/f5c781d979e01789ce626877044ca22e96fc11bffe260129c5f70313a424/click_option_group-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="e5dab79e3be37ede08962946cc87804501c442a6106579b6a743474269603add",
        url="https://pypi.org/packages/75/fc/86fe8cbd867896aa9db5b4ae659c5fea43abfa00fab2ae2b42fc92af9228/click_option_group-0.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")
        depends_on("py-click@7:", when="@0.5.3:")
        depends_on("py-click@7", when="@:0.5.2")
