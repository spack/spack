# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ripgrep(CargoPackage):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"

    # Pull ripgrep directly from crates.io for published releases
    crates_io = "ripgrep"
    # Can install master branch from GitHub
    git = "https://github.com/BurntSushi/ripgrep.git"

    version('master', branch='master')
    version('12.0.1', sha256='7dc6e92652933ac66d236d78ef61658b73c09639981bd1be0630461ce64d3cab')
    version('12.0.0', sha256='117f3608a82950b647d8f158cbd3388bffc0a594f29b2c39198392134126b6c0')
    version('11.0.2', sha256='d903146d825e92f77f95d1e1e8e5272f42253978c07d58c2294467a14dca126f')
