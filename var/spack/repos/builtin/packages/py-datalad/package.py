# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatalad(PythonPackage):
    """data distribution geared toward scientific datasets.

    DataLad makes data management and data distribution more accessible. To do
    that, it stands on the shoulders of Git and Git-annex to deliver a
    decentralized system for data exchange. This includes automated ingestion
    of data from online portals and exposing it in readily usable form as
    Git(-annex) repositories, so-called datasets. The actual data storage and
    permission management, however, remains with the original data providers.
    """

    homepage = "https://datalad.org/"
    pypi = "datalad/datalad-0.14.6.tar.gz"
    git = "https://github.com/datalad/datalad.git"

    version(
        "0.18.4",
        sha256="75bf85db017bb5cff0e62b6e75ba282bf04d061e1410017e132320dd6a4e79e4",
        url="https://pypi.org/packages/34/3a/639e37dc2c516342d4582ab9364aac948e235b661532ba56f3bd5f9a1d1b/datalad-0.18.4-py3-none-any.whl",
    )
    version(
        "0.18.3",
        sha256="a2607b592be02b7dbb5633484fd7055f3d7d6c1bd8c8490e80b85d49010ab69e",
        url="https://pypi.org/packages/b3/5d/0f639182dd8bf8c5c98e9010b366fe252a8f0f1a53983e37d9e04c379fa6/datalad-0.18.3-py3-none-any.whl",
    )
    version(
        "0.15.5",
        sha256="ab2d929887a5a1e04ab361740fe44dd60d2155c9a6938ae60490b67197e4711e",
        url="https://pypi.org/packages/54/cd/7336e65f5e8dab85406deb3955b268fe543114c7c61d7d99c617d0f072cc/datalad-0.15.5-py3-none-any.whl",
    )
    version(
        "0.15.3",
        sha256="ccd34eb26594c5f2aa3a7f5b562cde397a4e0f075bfff3d6685f8c6766051a5c",
        url="https://pypi.org/packages/e5/5f/84354ada51ca68c08af4b00ea88a2785417efa10cc94dace81df5df98c00/datalad-0.15.3-py3-none-any.whl",
    )
    version(
        "0.15.2",
        sha256="e8dbe5f940b704ef4c70043c499f30716b6e6d7d7287c12ea0c2c4ae5050108f",
        url="https://pypi.org/packages/fd/20/f4dc92cb59b047709256d6b8f3e6a473c0ac86aeb9f1dde6b02ba2bf4a68/datalad-0.15.2-py3-none-any.whl",
    )
    version(
        "0.15.1",
        sha256="afa91c75f7fd1e686e752e5272bc653e59037ee6644b8d48325e44dd17a225a3",
        url="https://pypi.org/packages/17/3f/2446b7699463bcafbc8a28b0b35f6fadc0dee4ca26b3a4b4884750e556b5/datalad-0.15.1-py3-none-any.whl",
    )
    version(
        "0.14.6",
        sha256="09b479a1411ce6464feef326059ab2bd70192851940808e168d16409181a56d8",
        url="https://pypi.org/packages/20/c6/8304d2a184e1f24aff1a4db9728f08c15a1bc02b3c698610ac3cdf9bc309/datalad-0.14.6-py3-none-any.whl",
    )

    variant("downloaders-extra", default=False, description="Enable extra downloaders support")
    variant("duecredit", default=False, description="Enable duecredit support")
    variant("full", default=False, description="Enable support for all available variants")
    variant(
        "metadata-extra", when="@:0.17", default=False, description="Enable extra metadata support"
    )
    variant("misc", default=False, description="Enable misc")
    variant("tests", default=False, description="Enable tests")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.16:")
        depends_on("py-annexremote", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-annexremote", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-appdirs", when="@0.14.6:0.14.7,0.15.1:0.15+full")
        depends_on("py-appdirs", when="@0.14.6:0.14.7,0.15.1:0.15")
        depends_on("py-argcomplete@1.12.3:", when="@0.17.10:+misc")
        depends_on("py-argcomplete@1.12.3:", when="@0.17.10:+full")
        depends_on("py-argcomplete", when="@0.14.7,0.15.1:0.15+misc")
        depends_on("py-argcomplete", when="@0.14.7,0.15.1:0.15+full")
        depends_on("py-beautifulsoup4", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+tests")
        depends_on("py-beautifulsoup4", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-boto", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-boto", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-chardet@3.0.4:", when="@0.14.6:0.14.7,0.15.1:0.15,0.18.2:+full")
        depends_on("py-chardet@3.0.4:", when="@0.14.6:0.14.7,0.15.1:0.15,0.18.2:")
        depends_on("py-colorama", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full platform=windows")
        depends_on("py-colorama", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10: platform=windows")
        depends_on("py-distro", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full ^python@3.8:")
        depends_on("py-distro", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10: ^python@3.8:")
        depends_on("py-duecredit", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-duecredit", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+duecredit")
        depends_on("py-exifread", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+metadata-extra")
        depends_on("py-exifread", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-fasteners@0.14:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-fasteners@0.14:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-httpretty@0.9.4:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+tests")
        depends_on("py-httpretty@0.9.4:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-humanize", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-humanize", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-importlib-metadata@3.6:", when="@0.17.10:+full ^python@:3.9")
        depends_on("py-importlib-metadata@3.6:", when="@0.17.10: ^python@:3.9")
        depends_on("py-importlib-metadata", when="@0.14.6:0.14.7,0.15.1:0.15+full ^python@:3.7")
        depends_on("py-importlib-metadata", when="@0.14.6:0.14.7,0.15.1:0.15 ^python@:3.7")
        depends_on("py-iso8601", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-iso8601", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-jsmin", when="@0.14.6:0.14.7+full")
        depends_on("py-jsmin", when="@0.14.6:0.14.7")
        depends_on("py-keyring@20:23.8,23.9.1:", when="@0.17.10:+full")
        depends_on("py-keyring@20:23.8,23.9.1:", when="@0.17.10:")
        depends_on("py-keyring@8:", when="@0.14.6:0.14.7,0.15.1:0.15+full")
        depends_on("py-keyring@8:", when="@0.14.6:0.14.7,0.15.1:0.15")
        depends_on("py-keyrings-alt", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-keyrings-alt", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-looseversion", when="@0.18:+full")
        depends_on("py-looseversion", when="@0.18:")
        depends_on("py-msgpack", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-msgpack", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on(
            "py-mutagen@1.36:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+metadata-extra"
        )
        depends_on("py-mutagen@1.36:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-mypy", when="@0.18.3:+tests")
        depends_on("py-mypy", when="@0.18.3:+full")
        depends_on("py-nose@1.3.4:", when="@0.14.6:0.14.7,0.15.1:0.15+tests")
        depends_on("py-nose@1.3.4:", when="@0.14.6:0.14.7,0.15.1:0.15+full")
        depends_on("py-packaging", when="@0.15.4:0.15,0.17.10:+full")
        depends_on("py-packaging", when="@0.15.4:0.15,0.17.10:")
        depends_on("py-patool", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-patool", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-pillow", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+metadata-extra")
        depends_on("py-pillow", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-platformdirs", when="@0.17.10:+full")
        depends_on("py-platformdirs", when="@0.17.10:")
        depends_on("py-pygithub", when="@0.14.6:0.14.7,0.15.1:0.15+full")
        depends_on("py-pygithub", when="@0.14.6:0.14.7,0.15.1:0.15")
        depends_on("py-pyperclip", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+misc")
        depends_on("py-pyperclip", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-pytest", when="@0.17.10:+tests")
        depends_on("py-pytest", when="@0.17.10:+full")
        depends_on("py-pytest-cov", when="@0.17.10:+tests")
        depends_on("py-pytest-cov", when="@0.17.10:+full")
        depends_on("py-pytest-fail-slow@0.2:", when="@0.17.10:+tests")
        depends_on("py-pytest-fail-slow@0.2:", when="@0.17.10:+full")
        depends_on("py-python-dateutil", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+misc")
        depends_on("py-python-dateutil", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-python-gitlab", when="@0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-python-gitlab", when="@0.14.7,0.15.1:0.15,0.17.10:")
        depends_on(
            "py-python-xmp-toolkit", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+metadata-extra"
        )
        depends_on("py-python-xmp-toolkit", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-pyyaml", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+metadata-extra")
        depends_on("py-pyyaml", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-requests@1.2:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-requests@1.2:", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:")
        depends_on("py-requests-ftp", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-requests-ftp", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+downloaders-extra")
        depends_on("py-simplejson", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-simplejson", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17")
        depends_on("py-tqdm", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.18+full")
        depends_on("py-tqdm", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.18")
        depends_on("py-types-python-dateutil", when="@0.17.10:+tests")
        depends_on("py-types-python-dateutil", when="@0.17.10:+full")
        depends_on("py-types-requests", when="@0.17.10:+tests")
        depends_on("py-types-requests", when="@0.17.10:+full")
        depends_on("py-typing-extensions@4:", when="@0.18.4:+full ^python@:3.10")
        depends_on("py-typing-extensions@4:", when="@0.18.4: ^python@:3.10")
        depends_on("py-typing-extensions", when="@0.18.3+full ^python@:3.9")
        depends_on("py-typing-extensions", when="@0.18.3 ^python@:3.9")
        depends_on("py-vcrpy", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+tests")
        depends_on("py-vcrpy", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:+full")
        depends_on("py-whoosh", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17+full")
        depends_on("py-whoosh", when="@0.14.6:0.14.7,0.15.1:0.15,0.17.10:0.17")
        depends_on("py-wrapt", when="@0.14.6:0.14.7,0.15.1:0.15+full")
        depends_on("py-wrapt", when="@0.14.6:0.14.7,0.15.1:0.15")

    # upper bound needed because otherwise the following error occurs:
    # 'extras_require' must be a dictionary whose values are strings or lists
    # of strings containing valid project/version requirement specifiers.

    # core

    # downloaders

    # publish

    # metadata

    # for version @:0.17

    # full
    # use conflict to avoid to have to maintain the dependencies twice
    conflicts("~downloaders-extra", when="+full")
    conflicts("~misc", when="+full")
    conflicts("~tests", when="+full")
    conflicts("~duecredit", when="+full")

    # for version @:0.17
    conflicts("~metadata-extra", when="+full")

    install_time_test_callbacks = ["test", "installtest"]

    def installtest(self):
        datalad = Executable(self.prefix.bin.datalad)
        datalad("wtf")
