# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand

arch = SpackCommand("arch")


def test_arch():
    """Sanity check ``spack arch`` to make sure it works."""

    arch()


def test_arch_platform():
    """Sanity check ``spack arch --platform`` to make sure it works."""

    arch("-p")
    arch("--platform")


def test_arch_operating_system():
    """Sanity check ``spack arch --operating-system`` to make sure it works."""

    arch("-o")
    arch("--operating-system")


def test_arch_target():
    """Sanity check ``spack arch --target`` to make sure it works."""

    arch("-t")
    arch("--target")


def test_display_targets():
    arch("--known-targets")
