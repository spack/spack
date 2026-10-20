# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Platform independent exceptions raised while creating or reading filesystem links."""


class SymlinkError(OSError):
    """Exception class for errors raised while creating symlinks,
    junctions and hard links
    """


class AlreadyExistsError(SymlinkError):
    """Link path already exists."""
