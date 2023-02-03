# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAttrs(Package, PythonExtension):
    """Classes Without Boilerplate"""

    homepage = "https://attrs.org/"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py2/a/attrs/attrs-22.2.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/attrs/"
    git = "https://github.com/python-attrs/attrs"

    version(
        "22.2.0",
        sha256="29e95c7f6778868dbd49170f98f8818f78f3dc5e0e37c0b1f474e3561b240836",
        expand=False,
    )
    version(
        "22.1.0",
        sha256="86efa402f67bf2df34f51a335487cf46b1ec130d02b8d39fd248abfd30da551c",
        expand=False,
    )
    version(
        "21.4.0",
        sha256="2d27e3784d7a565d36ab851fe94887c5eccd6a463168875832a1be79c82828b4",
        expand=False,
    )
    version(
        "21.2.0",
        sha256="149e90d6d8ac20db7a955ad60cf0e6881a3f20d37096140088356da6c716b0b1",
        expand=False,
    )
    version(
        "20.3.0",
        sha256="31b2eced602aa8423c2aea9c76a724617ed67cf9513173fd3a4f03e3a929c7e6",
        expand=False,
    )
    version(
        "20.2.0",
        sha256="fce7fc47dfc976152e82d53ff92fa0407700c21acd20886a13777a0d20e655dc",
        expand=False,
    )
    version(
        "20.1.0",
        sha256="2867b7b9f8326499ab5b0e2d12801fa5c98842d2cbd22b35112ae04bf85b4dff",
        expand=False,
    )
    version(
        "19.3.0",
        sha256="08a96c641c3a74e44eb59afb61a24f2cb9f4d7188748e76ba4bb5edfa3cb7d1c",
        expand=False,
    )
    version(
        "19.2.0",
        sha256="ec20e7a4825331c1b5ebf261d111e16fa9612c1f7a5e1f884f12bd53a664dfd2",
        expand=False,
    )
    version(
        "19.1.0",
        sha256="69c0dbf2ed392de1cb5ec704444b08a5ef81680a61cb899dc08127123af36a79",
        expand=False,
    )
    version(
        "18.1.0",
        sha256="4b90b09eeeb9b88c35bc642cbac057e45a5fd85367b985bd2809c62b7b939265",
        expand=False,
    )
    version(
        "16.3.0",
        sha256="c59426b15b45e39a7bc408eb6ba7e7188d9532764f873cc691199ddd975c97ef",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/a/attrs/attrs-{1}-{0}-none-any.whl"
        if version >= Version("22.2"):
            language = "py3"
        else:
            language = "py2.py3"
        return url.format(language, version)

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
