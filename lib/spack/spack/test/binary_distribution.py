# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util.filesystem import join_path

from spack.binary_distribution import get_buildfile_manifest
from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")


def test_text_relocate_if_needed(install_mockery, mock_fetch, monkeypatch, capfd):
    spec = Spec("needs-text-relocation").concretized()
    install(str(spec))

    manifest = get_buildfile_manifest(spec)
    assert join_path("bin", "exe") in manifest["text_to_relocate"]
    assert join_path("bin", "otherexe") not in manifest["text_to_relocate"]
    assert join_path("bin", "secretexe") not in manifest["text_to_relocate"]
