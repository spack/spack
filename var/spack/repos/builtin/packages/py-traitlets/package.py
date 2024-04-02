# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://github.com/ipython/traitlets"
    pypi = "traitlets/traitlets-5.0.4.tar.gz"

    version(
        "5.9.0",
        sha256="9e6ec080259b9a5940c797d58b613b5e31441c2257b87c2e795c5228ae80d2d8",
        url="https://pypi.org/packages/77/75/c28e9ef7abec2b7e9ff35aea3e0be6c1aceaf7873c26c95ae1f0d594de71/traitlets-5.9.0-py3-none-any.whl",
    )
    version(
        "5.7.1",
        sha256="57ba2ba951632eeab9388fa45f342a5402060a5cc9f0bb942f760fafb6641581",
        url="https://pypi.org/packages/cb/1e/7b8ae7bbc4c0d4b913cabb345c2ac98450bbd9cfe90ee2be275019037932/traitlets-5.7.1-py3-none-any.whl",
    )
    version(
        "5.3.0",
        sha256="65fa18961659635933100db8ca120ef6220555286949774b9cfc106f941d1c7a",
        url="https://pypi.org/packages/83/a9/1059771062cb80901c34a4dea020e76269412e69300b4ba12e3356865ad8/traitlets-5.3.0-py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="2d313cc50a42cd6c277e7d7dc8d4d7fedd06a2c215f78766ae7b1a66277e0033",
        url="https://pypi.org/packages/37/46/be8a3c030bd3673f4800fa7f46eda972dfa2990089a51ec5dd0a26ed33e9/traitlets-5.1.1-py3-none-any.whl",
    )
    version(
        "5.0.4",
        sha256="9664ec0c526e48e7b47b7d14cd6b252efa03e0129011de0a9c1d70315d4309c3",
        url="https://pypi.org/packages/e6/20/f73a1130598ffaf561fda74d761bbe66db7a3639f34456761e781509881b/traitlets-5.0.4-py3-none-any.whl",
    )
    version(
        "4.3.3",
        sha256="70b4c6a1d9019d7b4f6846832288f86998aa3b9207c6821f3578a6a6a467fe44",
        url="https://pypi.org/packages/ca/ab/872a23e29cec3cf2594af7e857f18b687ad21039c1f9b922fac5b9b142d5/traitlets-4.3.3-py2.py3-none-any.whl",
    )
    version(
        "4.3.2",
        sha256="c6cb5e6f57c5a9bdaa40fa71ce7b4af30298fbab9ece9815b5d995ab6217c7d9",
        url="https://pypi.org/packages/93/d6/abcb22de61d78e2fc3959c964628a5771e47e7cc60d53e9342e21ed6cc9a/traitlets-4.3.2-py2.py3-none-any.whl",
    )
    version(
        "4.3.1",
        sha256="50522e46dd7b66c80686d50ff1b774000f1d2a80c84b2bcfbd657d588e99a368",
        url="https://pypi.org/packages/b6/72/f62f13fb8cdb85af5239788d4c57c281b3a92efc9d2ad9cc44cb14c8c26d/traitlets-4.3.1-py2.py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="c13c85694e33272612c61f9d0f368eca63350b0300d7e3b9331f809f0fc360b5",
        url="https://pypi.org/packages/68/fe/a542484eb8d1b7b8949a06936f702dac80d316becc5d8416def728e13cea/traitlets-4.3.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="c6176a597361219f2f4cc1e82c560cc976c479b6f001fd851ac849391d6a648e",
        url="https://pypi.org/packages/ad/25/a507caa3514e7651fd14ffcffcd279779f604fefa3391b225bfb09d5c407/traitlets-4.2.2-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="05a66843c96a320eec09df674c16ff330a43cb07f731cf2bd88aa3645a180541",
        url="https://pypi.org/packages/db/f3/a24062437f01ceae74edf622ac3f8c55b555a2ed1967e5e3d945efe54c3d/traitlets-4.2.1-py2.py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="b920f170255dda49415f3ebf3caf666d3dadd08e38d490c84009792bd16d338f",
        url="https://pypi.org/packages/10/ed/37ca0815e846baea11d2cc65d7eeb127aef9c22f886847f151c372fc0d66/traitlets-4.2.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="0fdac5614e5cb3329a39d48bbbc4b95813920af7565c1488b5d787ef2863be26",
        url="https://pypi.org/packages/c7/ac/7bb361161e9b37d00a0b81f0e360fe0be8e2b9156e4da74aabf7f167b237/traitlets-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="5461707171e0f3c500c90eedef87d41e72a682da4894686d71825e16c824909d",
        url="https://pypi.org/packages/3a/9b/4a47994434b0f9f044c0cb44ebd5402a7cef4e02ff0662f7f5a2eeb6d484/traitlets-4.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5:5.9")
        depends_on("py-decorator", when="@4.1.0:4")
        depends_on("py-ipython-genutils", when="@4.1.0:5.0")
        depends_on("py-six", when="@4.3:4")
