# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hevea(MakefilePackage):
    """Hevea a fast Latex to HTML translator"""

    # Add a proper url for your package's homepage here.
    homepage = "http://hevea.inria.fr/"
    url      = "https://github.com/maranget/hevea/archive/v2.35.tar.gz"
    git      = "https://github.com/maranget/hevea.git"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['scemama', 'cessenat']

    # Add proper versions here.
    version('develop', branch='master')
    version('2.35', sha256='f189bada5d3e5b35855dfdfdb5b270c994fc7a2366b01250d761359ad66c9ecb')
    version('2.34', sha256='f505a2a5bafdc2ea389ec521876844e6fdcb5c1b656396b7e8421c1631469ea2')
    version('2.33', sha256='122f9023f9cfe8b41dd8965b7d9669df21bf41e419bcf5e9de5314f428380d0f')

    # Dependency demands ocamlbuild
    depends_on('ocaml')
    depends_on('ocamlbuild')

    def edit(self, spec, prefix):
        env['PREFIX'] = self.spec.prefix

    def build(self, spec, prefix):
        make()
