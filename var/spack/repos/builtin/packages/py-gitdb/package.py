# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGitdb(PythonPackage):
    """The GitDB project implements interfaces to allow read and write access
    to git repositories."""

    homepage = "https://gitdb.readthedocs.io"
    pypi = "gitdb/gitdb-4.0.5.tar.gz"

    license("BSD-3-Clause")

    version(
        "4.0.9",
        sha256="8033ad4e853066ba6ca92050b9df2f89301b8fc8bf7e9324d412a63f8bf1a8fd",
        url="https://pypi.org/packages/a3/7c/5d747655049bfbf75b5fcec57c8115896cb78d6fafa84f6d3ef4c0f13a98/gitdb-4.0.9-py3-none-any.whl",
    )
    version(
        "4.0.8",
        sha256="6875cbaed01f1b750394f372607803768fc7dad7c58c7ceb5f5917e980d779b2",
        url="https://pypi.org/packages/cf/22/8d2a2a2aa965252f6ae55a4ef2dd9fcf422c0d2b4e7f32b8a7c2d5ef5343/gitdb-4.0.8-py3-none-any.whl",
    )
    version(
        "4.0.7",
        sha256="6c4cc71933456991da20917998acbe6cf4fb41eeaab7d6d67fbc05ecd4c865b0",
        url="https://pypi.org/packages/ea/e8/f414d1a4f0bbc668ed441f74f44c116d9816833a48bf81d22b697090dba8/gitdb-4.0.7-py3-none-any.whl",
    )
    version(
        "4.0.6",
        sha256="27dea6c52fbcf768530e1af47f2e34afd24a52e53fa310c8279a5589bd7c85bd",
        url="https://pypi.org/packages/58/1a/b53069576a6b48a203ec8b7971ae5e455b1d801f5b7d086b986b8fc17186/gitdb-4.0.6-py3-none-any.whl",
    )
    version(
        "4.0.5",
        sha256="91f36bfb1ab7949b3b40e23736db18231bf7593edada2ba5c3a174a7b23657ac",
        url="https://pypi.org/packages/48/11/d1800bca0a3bae820b84b7d813ad1eff15a48a64caea9c823fc8c1b119e8/gitdb-4.0.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-smmap@3.0.1:5", when="@4.0.8:")
        depends_on("py-smmap@3.0.1:4", when="@4.0.7")
        depends_on("py-smmap@3.0.1:3", when="@4:4.0.6")
