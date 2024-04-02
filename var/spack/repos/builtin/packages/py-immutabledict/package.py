# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyImmutabledict(PythonPackage):
    """A fork of frozendict, an immutable wrapper around
    dictionaries. It implements the complete mapping interface and can be used as a
    drop-in replacement for dictionaries where immutability is
    desired. The immutabledict constructor mimics dict, and all of the
    expected interfaces (iter, len, repr, hash, getitem) are
    provided. Note that an immutabledict does not guarantee the
    immutability of its values, so the utility of hash method is
    restricted by usage. The only difference is that the copy() method
    of immutable takes variable keyword arguments, which will be
    present as key/value pairs in the new, immutable copy."""

    homepage = "https://github.com/corenting/immutabledict"
    pypi = "immutabledict/immutabledict-2.2.1.tar.gz"

    license("MIT")

    version(
        "2.2.1",
        sha256="8d7e32e0bda6dfb846349b78c753b858587c736f46be247d01ccd583ce5cc85b",
        url="https://pypi.org/packages/ea/ac/b443f0d19088968360df751113fa49646b597ab96ab466d73a281638a877/immutabledict-2.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:2.2.1")
