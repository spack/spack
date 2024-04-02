# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKornia(PythonPackage):
    """Open Source Differentiable Computer Vision Library for PyTorch."""

    homepage = "http://www.kornia.org/"
    pypi = "kornia/kornia-0.5.10.tar.gz"

    license("Apache-2.0")
    maintainers(
        "edgarriba",
        "ducha-aiki",
        "lferraz",
        "shijianjian",
        "cjpurackal",
        "johnnv1",
        "adamjstewart",
    )

    version(
        "0.7.2",
        sha256="411e09ccdc4efde351f90a81f35a6eb9fad3bcf58ac037cbec4d41a8364dd039",
        url="https://pypi.org/packages/ac/fa/5612c4b1ad83b3044062e9dd0ca3c91937d8023cff0836269e18573655b0/kornia-0.7.2-py2.py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="bd1cbe99373beafe6e59423be2374afbc2086a9ba57a8c66b94db6622b86f091",
        url="https://pypi.org/packages/34/5b/f1ee7ec4826cdd34f95f822c975f5a889c99dfd29491cebfc71db03b40e8/kornia-0.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="daa77a65f9cbfc1a67487d64a6b23d18a81f10eb94380312cda255d431bcc18a",
        url="https://pypi.org/packages/55/da/72cb83aa364ebb4d0109965e20c5d33d7063ccab15332c3fd0acfd5609c9/kornia-0.7.0-py2.py3-none-any.whl",
    )
    version(
        "0.6.12",
        sha256="659f0f0948e127b69ed437592f49531ccf4fc83d672474e1d89ed30d087e39e1",
        url="https://pypi.org/packages/e1/3f/967ecf8b43f81b8f60da48c84d48d9b724ecc7886fd9e0c645503116026f/kornia-0.6.12-py2.py3-none-any.whl",
    )
    version(
        "0.6.11",
        sha256="97bf856ab36ddac8dd249a359da34875aaf7d960b308c50f14d69d62053bf5a2",
        url="https://pypi.org/packages/3d/1a/359de937bcf3353d6a9e369aadc6946ce2f43c28ce3886383c22131f2597/kornia-0.6.11-py2.py3-none-any.whl",
    )
    version(
        "0.6.10",
        sha256="819ab431148442ee61954ba8772ac5ec2affbb6c956697a88da26666b912c0f0",
        url="https://pypi.org/packages/a3/73/555cafa4fb2f0eb3cb9de779bbe7cb120d36209268225d6acaf43ccec89d/kornia-0.6.10-py2.py3-none-any.whl",
    )
    version(
        "0.6.9",
        sha256="e60c64c0ae8073ac5cb767a497701a0a8c9fbe44b1da3072ea1cee41fe5e21b1",
        url="https://pypi.org/packages/c7/fb/c0f35b4b4e3ba6117b458a9cc8165575a5cb3f0ad9b3e14537407ffee7c2/kornia-0.6.9-py2.py3-none-any.whl",
    )
    version(
        "0.6.8",
        sha256="0d6d69330b4fd24da742337b8134da0ce01b4d7da66770db5498d58e8b4a0832",
        url="https://pypi.org/packages/99/03/3578e2f34d4ed63649bad6b15f9001d2d244e1f92c60a8dd5c5436e4402d/kornia-0.6.8-py2.py3-none-any.whl",
    )
    version(
        "0.6.7",
        sha256="e2908d888a3043bd6f950c514f00c1589f8d43cc25e4fb9b3ad1e66375146826",
        url="https://pypi.org/packages/7a/7f/5ec91cec58e02a41b1b0ea0fe9f0b2506cb68d497cf94382d464b2af77f4/kornia-0.6.7-py2.py3-none-any.whl",
    )
    version(
        "0.6.6",
        sha256="5e2356cf723af84280442d108b724313d21850c7b316ca3ceab192e36bcdef10",
        url="https://pypi.org/packages/72/14/6d2ffadce46ce40961d1d64f46a97faafc4093772b63e14333050843a2b6/kornia-0.6.6-py2.py3-none-any.whl",
    )
    version(
        "0.6.5",
        sha256="f79ca81824d8ca5704783a856f7bfb92ac1a17c7df8fe8d4c395767952d2678f",
        url="https://pypi.org/packages/50/33/89ebc68f8712c29dc451e79708451192b55e788ddfddfc1abbcab936e374/kornia-0.6.5-py2.py3-none-any.whl",
    )
    version(
        "0.6.4",
        sha256="642c0e8567ac305874fa05889523d906d761599d86e88b01558add744eb74dd4",
        url="https://pypi.org/packages/d9/d8/dfc513af1c6daf58049e740b5d71231f93a321670ea2dbf781d5fb3660a3/kornia-0.6.4-py2.py3-none-any.whl",
    )
    version(
        "0.6.3",
        sha256="c82c77cbc2dfe4aa537f794fb55560a71a2e08ae4047470de4f3ba330143d8b7",
        url="https://pypi.org/packages/9f/2d/0a7092331991ad1e7291e6adfcfed2d6bd639ad4c5f66385e477ccf0eb95/kornia-0.6.3-py2.py3-none-any.whl",
    )
    version(
        "0.6.2",
        sha256="5269279f6777aad92bd3926b333e5e8f6b7aee856eb95b6ec841364b673ae370",
        url="https://pypi.org/packages/89/d9/b78d36a1b1168170537c3220da0a2e09c191012526c162c119fa851e9cce/kornia-0.6.2-py2.py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="c896398fd2c3b4db08c4927a88f859925a24491d2e25476f62d8d4fa5a5a2a7e",
        url="https://pypi.org/packages/6d/ea/fcc3e64977446c9e27a8e2aca1070c495a0f660a57644ce680b95dd72ddc/kornia-0.6.1-py2.py3-none-any.whl",
    )
    version(
        "0.5.10",
        sha256="14ff44044bf07eb6f5b8dc5f5244e064bb02e5b05a500d161c495f69cfa607a4",
        url="https://pypi.org/packages/c0/98/ae65c5e539ca450d60489cda5f1d07f889b02b552140f97518a26e4c4230/kornia-0.5.10-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.7:")
        depends_on("python@3.7:", when="@0.6.9:0.6")
        depends_on("py-kornia-rs@0.1:", when="@0.7.2:")
        depends_on("py-packaging", when="@0.5.11:")
        depends_on("py-torch@1.9.1:", when="@0.6.9:")
        depends_on("py-torch@1.8.1:", when="@0.6:0.6.8")
        depends_on("py-torch@1.6:", when="@:0.5")

    # pyproject.toml

    # requirements/requirements.txt

    # Historical dependencies
