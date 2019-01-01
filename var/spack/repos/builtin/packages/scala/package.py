# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Scala(Package):
    """Scala is a general-purpose programming language providing support for
    functional programming and a strong static type system. Designed to be
    concise, many of Scala's design decisions were designed to build from
    criticisms of Java.
    """

    homepage = "https://www.scala-lang.org/"
    url = "https://downloads.lightbend.com/scala/2.12.1/scala-2.12.1.tgz"

    version('2.12.5', '25cf4989d061c585bd0a3fa357ccf0a6')
    version('2.12.1', '3eaecbce019b0fa3067503846e292b32')
    version('2.11.11', '3f5b76001f60cbc31111ddb81de5ea07')
    version('2.10.6', 'd79dc9fdc627b73289306bdaec81ca98')

    depends_on('java')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('lib')
        install_dir('doc')
        install_dir('man')
