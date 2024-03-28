# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbmake(PythonPackage):
    """Pytest plugin for testing notebooks."""

    homepage = "https://github.com/treebeardtech/nbmake"
    pypi = "nbmake/nbmake-0.5.tar.gz"

    license("Apache-2.0")

    version(
        "1.4.3",
        sha256="0318dd5dd30066e83717bf38888b2bec1b4744ad669a9801b41858e589493330",
        url="https://pypi.org/packages/96/50/5600dccaaed3de6faff6879b4236fcd56fc2ce3095662cd875bfc4288a47/nbmake-1.4.3-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="1c1619fc54a2fb64bfd84acbdf13b2ffba0e4a03bfea1684f4648f28ca850ada",
        url="https://pypi.org/packages/5d/40/6ef683d49d613fff75ee633a9b2cdfeafc6e02d59843e13f634a459c111c/nbmake-1.4.1-py3-none-any.whl",
    )
    version(
        "1.4",
        sha256="bc89fbc32484e761d95f26111e85237c6e9ed44b1cd26ba926e9502e5db4ace1",
        url="https://pypi.org/packages/c2/59/90766cd7b690ead86a3407bc68f1a5c044b0c3a907b286cb592400debc59/nbmake-1.4-py3-none-any.whl",
    )
    version(
        "1.3.5",
        sha256="8506d2a2d7eb55bdc0db0f1573039c734bd4f4d1c130df4ad8ade72b5b2a8fe0",
        url="https://pypi.org/packages/e9/79/c179e0cfb0a83cd905d805241acc74cc4960c9676c7331b52ceac05da0cc/nbmake-1.3.5-py3-none-any.whl",
    )
    version(
        "1.3.4",
        sha256="88f263ecf3dadb80141c7653626cf056db3f731513c69674cf4e7b8bdb483e61",
        url="https://pypi.org/packages/87/26/8d1f300c340027f5a6c8473f04b7d5487fec3b9e4766791ad20e6d50679f/nbmake-1.3.4-py3-none-any.whl",
    )
    version(
        "1.3.3",
        sha256="2f1cf4715ff24a5acd8929b4b71a9867e1e5efec5e4c74f51ceb2bacc6eb1c4d",
        url="https://pypi.org/packages/4b/fd/514136df225f6008cc08faa719ac79a0358167526f75c55cc453a25946f6/nbmake-1.3.3-py3-none-any.whl",
    )
    version(
        "1.3.2",
        sha256="a7538fb695c079d59669b798d81ff3f7dd7096e99af8a6b778d7cb21fc7eab01",
        url="https://pypi.org/packages/7e/3d/be2d58e34bf6e80637a0af578c905e7c5269bbd03ac18e7e034fe31cd9ea/nbmake-1.3.2-py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="8cdb32a09f31c8b00e6e36fc082ba24ffdfdc306fa84aad797bb3dc45352b52f",
        url="https://pypi.org/packages/76/cc/6701e5b083d24092b996915bcf203adcb097a3826ba3f7a233e7ebcf55d4/nbmake-1.3.1-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="8b38089dd232142ce894a9ad3e57a7c0f0a0edb0254662a8446346a84ac4079d",
        url="https://pypi.org/packages/74/9c/97f973b5b0ec7f5546443fd896010471ace61d00cb002a886c68bd410d9a/nbmake-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="8966b11098af6e5eb3270075f28c22901e3c9df3688d42beafb9be25e3027fcf",
        url="https://pypi.org/packages/b7/31/57e138dd825f95d884bddd16a0be8fa8bde20fa76e96e196549f241b1d0d/nbmake-1.2.1-py3-none-any.whl",
    )
    version(
        "1.2",
        sha256="d011d0ef26c4b13b13f3c37806f6345ba71e9dd7ece224349c6546c0e76650b9",
        url="https://pypi.org/packages/11/26/132c5198804c56b53947df435198c66e88c048412eae4b6c7cb4ddc52b86/nbmake-1.2-py3-none-any.whl",
    )
    version(
        "1.1",
        sha256="04603dd8b7894830f7079b317bc81df29b15ddd0db014279c58145b6fce80d7a",
        url="https://pypi.org/packages/57/9e/68a36c3610496029dc6e310545938e91ea5a4572cd5aa681d472d31f86e8/nbmake-1.1-py3-none-any.whl",
    )
    version(
        "1.0",
        sha256="4d4102d5b41194be8ac96bb4400dd0c6705f77d6b4c9ffb207daf79409684752",
        url="https://pypi.org/packages/e7/2d/cf336b8ab86599171e86570880bafd0e172fc6b660311097b6127a892125/nbmake-1.0-py3-none-any.whl",
    )
    version(
        "0.10",
        sha256="7e7625364be84f646741bc8934adb2905b6f5063d434034985cc08f581234225",
        url="https://pypi.org/packages/be/c4/44d4b1804b53a373cf9bda3eeebc5daf248cf71fd3341afbf56c8959f95f/nbmake-0.10-py3-none-any.whl",
    )
    version(
        "0.9",
        sha256="fcae85ec12b077cbb5a23f67091748a5a2e68ce35fe1b5fa14789d2067c7eb7f",
        url="https://pypi.org/packages/93/33/ddf620b8ca2b934a67501764088deba7a81ba57258dd68caf0b92f3c4a65/nbmake-0.9-py3-none-any.whl",
    )
    version(
        "0.8",
        sha256="94d24574ea465eb62e96086dba444829c00190ace33dc53e5c3b608fe8e85498",
        url="https://pypi.org/packages/e6/4d/851bc6290e61b5a85c2398f6e75a172c3848ed546ed1868625c9c4ac5123/nbmake-0.8-py3-none-any.whl",
    )
    version(
        "0.7",
        sha256="dbde6ab506c0133a84cab6911dff0bc75ca814ba386f162a900f3b5e7b6c1b7f",
        url="https://pypi.org/packages/9a/aa/462be8e18d97e7b673e8e85a53a5a102d3e22ac02bc879742c625fadee2f/nbmake-0.7-py3-none-any.whl",
    )
    version(
        "0.6",
        sha256="f9febf7e8994b96da1b3afc8a0993484458f4ebb9ea8ef0758c17b0f8c8b4c4d",
        url="https://pypi.org/packages/91/3a/d2c30290736c1439865823830d9612b9444b988da1fe194dc94f9c134f5a/nbmake-0.6-py3-none-any.whl",
    )
    version(
        "0.5",
        sha256="8a0b3ce9ca26320165c6de532c3d36445da1dd53c2c8fac4870ed900b3cbe538",
        url="https://pypi.org/packages/00/79/f0d7bd40a3cfbdb5f05d4611c18fdfaec32efa02c5bde9fad3745d2773d7/nbmake-0.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ipykernel@5.4:", when="@0.7:")
        depends_on("py-ipykernel@5.4:5", when="@0.1:0.5")
        depends_on("py-nbclient@0.6.6:0.6", when="@1.3.1:")
        depends_on("py-nbclient@0.5.13:0.5", when="@1.3:1.3.0")
        depends_on("py-nbclient@0.5.5:0.5", when="@1.2")
        depends_on("py-nbclient@0.3:", when="@0.2:1.1")
        depends_on("py-nbformat@5.0.8:", when="@0.1:")
        depends_on("py-pathlib@1.0.1:", when="@:0.0.1.0,0.1:0.8")
        depends_on("py-pydantic@1.7.2:1", when="@:0.0.1.0,0.1:1.4.1")
        depends_on("py-pygments@2.7.3:", when="@0.1:")
        depends_on("py-pytest@6.1:", when="@1.2.1:")
        depends_on("py-pytest@6.1:6", when="@0.10:1.2.0")
        depends_on("py-pytest@6.1.2:6", when="@0.1:0.9")

    # Historical dependencies
