# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingExtensions(PythonPackage):
    """The typing_extensions module contains both backports of these
    changes as well as experimental types that will eventually be
    added to the typing module, such as Protocol (see PEP 544 for
    details about protocols and static duck typing)."""

    homepage = "https://github.com/python/typing_extensions"
    pypi = "typing_extensions/typing_extensions-3.7.4.tar.gz"

    license("0BSD")

    version(
        "4.8.0",
        sha256="8f92fc8806f9a6b641eaa5318da32b44d401efaac0f6678c9bc448ba3605faa0",
        url="https://pypi.org/packages/24/21/7d397a4b7934ff4028987914ac1044d3b7d52712f30e2ac7a2ae5bc86dd0/typing_extensions-4.8.0-py3-none-any.whl",
    )
    version(
        "4.6.3",
        sha256="88a4153d8505aabbb4e13aacb7c486c2b4a33ca3b3f807914a9b4c844c471c26",
        url="https://pypi.org/packages/5f/86/d9b1518d8e75b346a33eb59fa31bdbbee11459a7e2cc5be502fa779e96c5/typing_extensions-4.6.3-py3-none-any.whl",
    )
    version(
        "4.5.0",
        sha256="fb33085c39dd998ac16d1431ebc293a8b3eedd00fd4a32de0ff79002c19511b4",
        url="https://pypi.org/packages/31/25/5abcd82372d3d4a3932e1fa8c3dbf9efac10cc7c0d16e78467460571b404/typing_extensions-4.5.0-py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="25642c956049920a5aa49edcdd6ab1e06d7e5d467fc00e0506c44ac86fbfca02",
        url="https://pypi.org/packages/ed/d6/2afc375a8d55b8be879d6b4986d4f69f01115e795e36827fd3a40166028b/typing_extensions-4.3.0-py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="6657594ee297170d19f67d55c05852a874e7eb634f4f753dbd667855e07c1708",
        url="https://pypi.org/packages/75/e1/932e06004039dd670c9d5e1df0cd606bf46e29a28e65d5bb28e894ea29c9/typing_extensions-4.2.0-py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="21c85e0fe4b9a155d0799430b0ad741cdce7e359660ccbd8b530613e8df88ce2",
        url="https://pypi.org/packages/45/6b/44f7f8f1e110027cf88956b59f2fad776cca7e1704396d043f89effd3a0e/typing_extensions-4.1.1-py3-none-any.whl",
    )
    version(
        "3.10.0.2",
        sha256="f1d25edafde516b146ecd0613dabcc61409817af4766fbbcfb8d1ad4ec441a34",
        url="https://pypi.org/packages/74/60/18783336cc7fcdd95dae91d73477830aa53f5d3181ae4fe20491d7fc3199/typing_extensions-3.10.0.2-py3-none-any.whl",
    )
    version(
        "3.10.0.0",
        sha256="779383f6086d90c99ae41cf0ff39aac8a7937a9283ce0a414e5dd782f4c94a84",
        url="https://pypi.org/packages/2e/35/6c4fff5ab443b57116cb1aad46421fb719bed2825664e8fe77d66d99bcbc/typing_extensions-3.10.0.0-py3-none-any.whl",
    )
    version(
        "3.7.4.3",
        sha256="7cb407020f00f7bfc3cb3e7881628838e69d8f3fcab2f64742a5e76b2f841918",
        url="https://pypi.org/packages/60/7a/e881b5abb54db0e6e671ab088d079c57ce54e8a01a3ca443f561ccadb37e/typing_extensions-3.7.4.3-py3-none-any.whl",
    )
    version(
        "3.7.4",
        sha256="d8179012ec2c620d3791ca6fe2bf7979d979acdbef1fca0bc56b37411db682ed",
        url="https://pypi.org/packages/27/aa/bd1442cfb0224da1b671ab334d3b0a4302e4161ea916e28904ff9618d471/typing_extensions-3.7.4-py3-none-any.whl",
    )
    version(
        "3.7.2",
        sha256="f3f0e67e1d42de47b5c67c32c9b26641642e9170fe7e292991793705cd5fef7c",
        url="https://pypi.org/packages/0f/62/c66e553258c37c33f9939abb2dd8d2481803d860ff68e635466f12aa7efa/typing_extensions-3.7.2-py3-none-any.whl",
    )
    version(
        "3.6.6",
        sha256="55401f6ed58ade5638eb566615c150ba13624e2f0c1eedd080fc3c1b6cb76f1d",
        url="https://pypi.org/packages/62/4f/392a1fa2873e646f5990eb6f956e662d8a235ab474450c72487745f67276/typing_extensions-3.6.6-py3-none-any.whl",
    )
