# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install changa
#
# You can edit this file again by typing:
#
#     spack edit changa
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Changa(AutotoolsPackage):
    """ChaNGa (Charm N-body GrAvity solver) is a code to perform collisionless N-body simulations.
    It can perform cosmological simulations with periodic boundary conditions in comoving coordinates
    or simulations of isolated stellar systems. It also can include hydrodynamics using the
    Smooth Particle Hydrodynamics (SPH) technique. It uses a Barnes-Hut tree to calculate gravity,
    with hexadecapole expansion of nodes and Ewald summation for periodic forces.
    Timestepping is done with a leapfrog integrator with individual timesteps for each particle."""

    homepage = "http://faculty.washington.edu/trq/hpcc/tools/changa.html"
    url      = "https://github.com/N-BodyShop/changa/archive/v3.4.tar.gz"
    git      = "https://github.com/N-BodyShop/changa.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('3.4', sha256='c2bceb6ac00025dfd704bb6960bc17c6df7c746872185845d1e75f47e6ce2a94')
    patch("fix_configure_path.patch")

    resource(
            name="utility",
            url="https://github.com/N-BodyShop/utility/archive/v3.4.tar.gz",
            sha256="19f9f09023ce9d642e848a36948788fb29cd7deb8e9346cdaac4c945f1416667",
            placement="utility"
            )

    depends_on("charmpp build-target=ChaNGa")
    #depends_on("libtirpc")
    """
    @run_before('configure')
    def cleanup(self):
        if os.path.isfile('Makefile'):
            make('dist-clean')
    """

    def configure_args(self):
        args = []
        args.append("STRUCT_DIR={}/utility/structures".format(self.stage.source_path))
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            copy('ChaNGa', prefix.bin)
            copy('charmrun', prefix.bin)


