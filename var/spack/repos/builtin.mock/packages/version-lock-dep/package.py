# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class VersionLockDep(Package):
    """version-lock-dep is depended on by version-lock with the same version"""

    homepage = "http://example.com/version-lock-dep/"
    url = "http://example.com/version-lock-dep.tar.gz"

    version("3.2.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("3.2.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("3.1.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("3.1.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("3.0.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")

    version("2.2.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("2.2.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("2.1.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("2.1.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("2.0.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")

    version("1.2.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("1.2.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("1.1.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("1.1.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("1.0.0", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
