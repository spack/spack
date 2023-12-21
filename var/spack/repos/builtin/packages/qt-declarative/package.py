# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtDeclarative(QtPackage):
    """Qt Declarative (Quick 2)."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    version("6.6.1", sha256="b1f5a75c2ea967d21b2c45f56ba1de66e2bf14a581b2f0d8e776441f1bebd0e7")
    version("6.6.0", sha256="2e52ef00736a9954426adf454cfb365fabdffb5703c814c188bc866cbf9f4dad")
    version("6.5.3", sha256="563924e58ac517492acb1952af0fb950cd54045ef6d61b98de06fac728239811")
    version("6.5.2", sha256="8b9eed849c90fb301d5399c545c2c926c18dc889d724df2b284253152a2ee139")
    version("6.5.1", sha256="b6f81ee73e8dbc30601c022b30ceb592fd2f8a5a79e7bc48fcd7feef80e3cc7a")
    version("6.5.0", sha256="38281cdfc60b8820ac2943eebabe968138f90629edc8c6c5e88a72a7ec05e303")
    version("6.4.3", sha256="9549668f8ec28199ba19d73fb535855dc5bea690097f43c2f91954bc27ee0fa3")
    version("6.4.2", sha256="dec3599b55f75cff044cc6384fa2f7e9505f8a48af1b4c185c2789e2dafabda6")
    version("6.4.1", sha256="23b5c91e98ec2b8a4118a3d3ace0c2e61b355cc8f2ccb87d189708b69446f917")
    version("6.4.0", sha256="daf7b97be51451af5afa35e1c0421fb8964003852088b0293c144a12bd664cd1")
    version("6.3.2", sha256="140a3c4973d56d79abf5fea9ae5cf13b3ef7693ed1d826b263802926a4ba84b6")
    version("6.3.1", sha256="1606723c2cc150c9b7339fd33ca5e2ca00d6e738e119c52a1d37ca12d3329ba9")
    version("6.3.0", sha256="b7316d6c195fdc31ecbf5ca2acf2888737539919a02ff8f11a911432d50c17ac")
    version("6.2.4", sha256="cd939d99c37e7723268804b9516e32f8dd64b985d847469c78b66b5f4481c548")
    version("6.2.3", sha256="eda82abfe685a6ab5664e4268954622ccd05cc9ec8fb16eaa453c54900591baf")

    # Testing requires +network
    depends_on("qt-base +network", type="test")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-shadertools@" + v, when="@" + v)
