# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ShinyServer(CMakePackage):
    """Shiny server lets you put shiny web applications and interactive
       documents online. Take your shiny apps and share them with your
       organization or the world."""

    #
    # HEADS UP:
    # 1. The shiny server installation step will download various node
    #    and npm bits from the net.  They seem to have them well
    #    constrained ("npm shrinkwrap"?), but this package is not
    #    "air gappable".
    # 2. Docs say that it requires 'gcc'.  depends_on() won't do the
    #    right thing, it's Up To You.
    #
    homepage = "https://www.rstudio.com/products/shiny/shiny-server/"
    url = "https://github.com/rstudio/shiny-server/archive/v1.5.3.838.tar.gz"

    version('1.5.16.958', sha256='b42d39e38e08cb7cee132583751e0b04e639df17a4bbf3654387653761a31139')
    version('1.5.15.953', sha256='fcd48b5a77db1345a7d817a2377bd51c14c16f05ea5a1f6e1aa00eeaef82990e')
    version('1.5.14.948', sha256='43fa489cb953df3ff7f21d93542e1ff3c81566268605f63c2b61b488a684e5c0')
    version('1.5.13.944', sha256='938c45f60fe7f5e27bccd1a8e16c546c49d4800e3f4e2bbdbdf408c475abf379')
    version('1.5.12.933', sha256='59dd03b2d908d7147e74092145b474d671c4806a6a959b5b95723cde91ed2d50')
    version('1.5.9.923',  sha256='11aa809227c161125f1000fff492d2341da2cd31cbfe9b321034804d70bf50af')
    version('1.5.8.921',  sha256='64d1ab0881a02877d46b2c5070fa1bac75acf94b37e93877212fa9fe400fc69b')
    version('1.5.7.907',  sha256='e39604adb29432c5cd28d21835ea0cdc934d23b573cb9530f90dd93fa0b9f93e')
    version('1.5.6.875',  sha256='58fd3cd06630d69208213957d8ca56f7457cef5bd235836aab7b8a5edfc609b8')
    version('1.5.5.872',  sha256='4268c0d5455be518c8b33efd3454af0e99870a5e599315251843e481df72cd4d')
    version('1.5.3.838', sha256='6fd1b12cd1cbe5c64cacbec4accefe955353f9c675e5feff809c0e911a382141')

    depends_on('python@:2.8')  # docs say: "Really.  3.x will not work"
    depends_on('cmake@2.8.10:', type='build')
    depends_on('git')
    depends_on('r+X')
    depends_on('openssl')

    def cmake_args(self):
        spec = self.spec
        options = []

        options.append("-DPYTHON=%s" % spec['python'].command.path)

        return options

    # Recompile the npm modules included in the project
    @run_after('build')
    def build_node(self):
        bash = which('bash')
        mkdirp('build')
        bash('-c', 'bin/npm --python="$PYTHON" install')
        bash('-c', 'bin/node ./ext/node/lib/node_modules/npm/node_modules/node-gyp/bin/node-gyp.js --python="$PYTHON" rebuild')  # noqa: E501

    def setup_run_environment(self, env):
        env.prepend_path('PATH', join_path(self.prefix, 'shiny-server', 'bin'))
        # shiny comes with its own pandoc; hook it up...
        env.prepend_path('PATH', join_path(
            self.prefix, 'shiny-server', 'ext', 'pandoc', 'static'))
