##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os
import platform
import shutil
import sys
from spack import *


class Charm(Package):
    """Charm++ is a parallel programming framework in C++ supported by
    an adaptive runtime system, which enhances user productivity and
    allows programs to run portably from small multicore computers
    (your laptop) to the largest supercomputers."""

    homepage = "http://charmplusplus.org"
    url      = "http://charm.cs.illinois.edu/distrib/charm-6.7.1.tar.gz"

    version("6.7.1", "a8e20cf85e9c8721158f5bbd0ade48d9")
    version("6.7.0", "35a39a7975f1954a7db2d76736158231")
    version("6.6.1", "9554230f741e2599deaaac4d9d93d7ab")
    version("6.6.0", "31e95901b3f7324d52107e6ad000fcc8")
    version("6.5.1", "034d99458474a3ab96d8bede8a691a5d")

    # Support OpenMPI; see
    # <https://charm.cs.illinois.edu/redmine/issues/1206>
    patch("mpi.patch")
    # Ignore compiler warnings while configuring
    patch("strictpass.patch")

    # Communication mechanisms (choose exactly one)
    # TODO: Support Blue Gene/Q PAMI, Cray GNI, Cray shmem, CUDA
    variant("mpi", default=True,
            description="Use MPI as communication mechanism")
    variant("multicore", default=False,
            description="Disable inter-node communication")
    variant("net", default=False,
            description="Use net communication mechanism")
    variant("netlrts", default=True,
            description="Use netlrts communication mechanism")
    variant("verbs", default=False,
            description="Use Infiniband as communication mechanism")

    # Other options
    # Something is off with PAPI -- there are build errors. Maybe
    # Charm++ expects a particular version?
    variant("papi", default=False, description="Enable PAPI integration")
    variant("smp", default=True,
            description=(
                "Enable SMP parallelism (does not work with +multicore)"))
    variant("tcp", default=False,
            description="Use TCP as transport mechanism (requires +net)")

    # Note: We could add variants for AMPI, LIBS, bigemulator, msa, Tau
    # Note: We could support shared libraries

    depends_on("mpi", when="+mpi")
    depends_on("papi", when="+papi")

    def install(self, spec, prefix):
        target = "charm++"

        # Note: Turn this into a multi-valued variant, once these
        # exist in Spack
        if sum(["+mpi" in spec,
                "+multicore" in spec,
                "+net" in spec,
                "+netlrts" in spec,
                "+verbs" in spec]) != 1:
            raise InstallError(
                "Exactly one communication mechanism "
                "(+mpi, +multicore, +net, +netlrts, or +verbs) "
                "must be enabled")
        if "+mpi" in spec:
            comm = "mpi"
        if "+multicore" in spec:
            comm = "multicore"
        if "+net" in spec:
            comm = "net"
        if "+netlrts" in spec:
            comm = "netlrts"
        if "+verbs" in spec:
            comm = "verbs"

        plat = sys.platform
        if plat.startswith("linux"):
            plat = "linux"
        mach = platform.machine()

        # Define Charm++ version names for various (plat, mach, comm)
        # combinations. Note that not all combinations are supported.
        versions = {
            ("darwin", "i386", "multicore"): "multicore-darwin-x86",
            ("darwin", "i386", "net"): "net-darwin-x86",
            ("darwin", "x86_64", "mpi"): "mpi-darwin-x86_64",
            ("darwin", "x86_64", "multicore"): "multicore-darwin-x86_64",
            ("darwin", "x86_64", "net"): "net-darwin-x86_64",
            ("darwin", "x86_64", "netlrts"): "netlrts-darwin-x86_64",
            ("linux", "i386", "mpi"): "mpi-linux",
            ("linux", "i386", "multicore"): "multicore-linux32",
            ("linux", "i386", "net"): "net-linux",
            ("linux", "i386", "netlrts"): "netlrts-linux",
            ("linux", "x86_64", "mpi"): "mpi-linux-x86_64",
            ("linux", "x86_64", "multicore"): "multicore-linux64",
            ("linux", "x86_64", "net"): "net-linux-x86_64",
            ("linux", "x86_64", "netlrts"): "netlrts-linux-x86_64",
            ("linux", "x86_64", "verbs"): "verbs-linux-x86_64",
        }
        if (plat, mach, comm) not in versions:
            raise InstallError(
                "The communication mechanism %s is not supported "
                "on a %s platform with a %s CPU" %
                (comm, plat, mach))
        version = versions[(plat, mach, comm)]

        # We assume that Spack's compiler wrappers make this work. If
        # not, then we need to query the compiler vendor from Spack
        # here.
        compiler = "gcc"

        options = [compiler,
                   "--with-production",   # Note: turn this into a variant
                   "-j%d" % make_jobs,
                   "--destination=%s" % prefix]
        if "+mpi" in spec:
            options.append("--basedir=%s" % spec["mpi"].prefix)
        if "+papi" in spec:
            options.extend(["papi", "--basedir=%s" % spec["papi"].prefix])
        if "+smp" in spec:
            if "+multicore" in spec:
                # This is a Charm++ limitation; it would lead to a
                # build error
                raise InstallError("Cannot combine +smp with +multicore")
            options.append("smp")
        if "+tcp" in spec:
            if "+net" not in spec:
                # This is a Charm++ limitation; it would lead to a
                # build error
                raise InstallError(
                    "The +tcp variant requires "
                    "the +net communication mechanism")
            options.append("tcp")

        # Call "make" via the build script
        # Note: This builds Charm++ in the "tmp" subdirectory of the
        # install directory. Maybe we could set up a symbolic link
        # back to the build tree to prevent this? Alternatively, we
        # could dissect the build script; the build instructions say
        # this wouldn't be difficult.
        build = Executable(join_path(".", "build"))
        build(target, version, *options)

        # Charm++'s install script does not copy files, it only creates
        # symbolic links. Fix this.
        for dirpath, dirnames, filenames in os.walk(prefix):
            for filename in filenames:
                filepath = join_path(dirpath, filename)
                if os.path.islink(filepath):
                    tmppath = filepath + ".tmp"
                    # Skip dangling symbolic links
                    try:
                        shutil.copy2(filepath, tmppath)
                        os.remove(filepath)
                        os.rename(tmppath, filepath)
                    except:
                        pass
        shutil.rmtree(join_path(prefix, "tmp"))
