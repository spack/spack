# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Atompaw(Package):
    """A Projector Augmented Wave (PAW) code for generating
    atom-centered functions.

    Official website: http://pwpaw.wfu.edu

    User's guide: ~/doc/atompaw-usersguide.pdf
    """
    homepage = "http://users.wfu.edu/natalie/papers/pwpaw/man.html"
    url = "http://users.wfu.edu/natalie/papers/pwpaw/atompaw-4.0.0.13.tar.gz"

    version('4.0.0.13', 'af4a042380356f6780183c4b325aad1d')
    version('3.1.0.3', 'c996a277e11707887177f47bbb229aa6')

    depends_on("lapack")
    depends_on("blas")

    # pin libxc version
    depends_on("libxc@2.2.1")

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]

        linalg = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            "--with-linalg-libs=%s" % linalg.ld_flags,
            "--enable-libxc",
            "--with-libxc-incs=-I%s" % spec["libxc"].prefix.include,
            "--with-libxc-libs=-L%s -lxcf90 -lxc" % spec["libxc"].prefix.lib,
        ])

        configure(*options)
        make(parallel=False)  # parallel build fails
        make("check")
        make("install")
