# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PerlModuleBuild(PerlPackage):
    """Module::Build is a system for building, testing, and installing Perl
    modules. It is meant to be an alternative to ExtUtils::MakeMaker.
    Developers may alter the behavior of the module through subclassing in a
    much more straightforward way than with MakeMaker. It also does not
    require a make on your system - most of the Module::Build code is
    pure-perl and written in a very cross-platform way.
    """

    homepage = "http://search.cpan.org/perldoc/Module::Build"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/Module-Build-0.4224.tar.gz"

    version('0.4231', sha256='7e0f4c692c1740c1ac84ea14d7ea3d8bc798b2fb26c09877229e04f430b2b717')
    version('0.4229', sha256='1fe491a6cda914b01bc8e592faa2b5404e9f35915ca15322f8f2a8d8f9008c18')
    version('0.4224', sha256='a6ca15d78244a7b50fdbf27f85c85f4035aa799ce7dd018a0d98b358ef7bc782')
    version('0.4220', sha256='fb1207c7e799366f7a8adda3f135bf8141c4d6068505650d4db2b2d3ce34b5a2')
