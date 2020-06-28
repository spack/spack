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
    crates_io = "ripgrep"
    git = "https://github.com/BurntSushi/ripgrep.git"

    maintainers = ["AndrewGaspar"]

    version('master', branch='master')
    version('12.1.1', sha256='b955557adc78324dbc2bc663ca85df54b48a579b340876e38dffb39f24882ebf')
