# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDirExpiry(RPackage):
    """Managing Expiration for Cache Directories.

    Implements an expiration system for access to versioned directories.
    Directories that have not been accessed by a registered function within a
    certain time frame are deleted. This aims to reduce disk usage by
    eliminating obsolete caches generated by old versions of packages."""

    bioc = "dir.expiry"

    version("1.8.0", commit="271f76cb2e8565817400e85fcc2c595923af4af6")

    depends_on("r-filelock", type=("build", "run"))
