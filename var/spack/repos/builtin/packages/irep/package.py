# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class Irep(CMakePackage):
    """IREP is a tool that enables mixed-language simulation codes to use a
    common, Lua-based format for their input decks. Essentially, the input
    format is a set of tables -- Lua's one (and only?) data structure."""

    homepage = "https://irep.readthedocs.io/"
    git      = "https://github.com/LLNL/irep.git"

    maintainers = ['tomstitt', 'kennyweiss']

    version('master', branch='master')

    depends_on('lua-luajit', type=('link', 'run'))
    depends_on('lua', type=('link', 'run'))
