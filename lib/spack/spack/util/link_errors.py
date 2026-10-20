# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Platform independent exceptions raised while creating or reading filesystem links."""

import errno


class SymlinkError(OSError):
    """Exception class for errors raised while creating symlinks,
    junctions and hard links
    """


class AlreadyExistsError(SymlinkError, FileExistsError):
    """Link path already exists."""

    def __init__(self, *args):
        super().__init__(*args)
        self.errno = errno.EEXIST
