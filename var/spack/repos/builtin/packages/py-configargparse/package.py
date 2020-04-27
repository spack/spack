# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-configargparse
#
# You can edit this file again by typing:
#
#     spack edit py-configargparse
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyConfigargparse(PythonPackage):
    """Applications with more than a handful of user-settable
    options are best configured through a combination of
    command line args, config files, hard-coded defaults, and
    in some cases, environment variables.

    Python's command line parsing modules such as argparse have
    very limited support for config files and environment
    variables, so this module extends argparse to add these
    features."""

    homepage = "https://github.com/bw2/ConfigArgParse"
    url      = "https://github.com/bw2/ConfigArgParse/archive/1.2.3.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.2.3', sha256='0f1144a204e3b896d6ac900e151c1d13bde3103d6b7d541e3bb57514a94083bf')

    depends_on('python@2.2:2.999,3.5:', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
