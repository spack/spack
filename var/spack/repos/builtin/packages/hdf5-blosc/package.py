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
import shutil
import sys

from spack import *


def _install_shlib(name, src, dst):
    """Install a shared library from directory src to directory dst"""
    if sys.platform == "darwin":
        shlib0 = name + ".0.dylib"
        shlib = name + ".dylib"
        shutil.copyfile(join_path(src, shlib0), join_path(dst, shlib0))
        os.symlink(shlib0, join_path(dst, shlib))
    else:
        shlib000 = name + ".so.0.0.0"
        shlib0 = name + ".so.0"
        shlib = name + ".dylib"
        shutil.copyfile(join_path(src, shlib000), join_path(dst, shlib000))
        os.symlink(shlib000, join_path(dst, shlib0))
        os.symlink(shlib0, join_path(dst, shlib))


class Hdf5Blosc(Package):
    """Blosc filter for HDF5"""
    homepage = "https://github.com/Blosc/hdf5-blosc"
    url      = "https://github.com/Blosc/hdf5-blosc"

    version('master', git='https://github.com/Blosc/hdf5-blosc',
            branch='master')

    depends_on("c-blosc")
    depends_on("hdf5")
    depends_on("libtool", type='build')

    parallel = False

    def install(self, spec, prefix):
        # The included cmake recipe doesn"t work for Darwin
        # cmake(".", *std_cmake_args)
        #
        # make()
        # make("install")
        # if sys.platform == "darwin":
        #     fix_darwin_install_name(prefix.lib)

        libtool = Executable(join_path(spec["libtool"].prefix.bin, "libtool"))

        # TODO: these vars are not used.
        # if "+mpi" in spec["hdf5"]:
        #     cc = "mpicc"
        # else:
        #     cc = "cc"
        # shlibext = "so" if sys.platform != "darwin" else "dylib"

        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        # Build and install filter
        with working_dir("src"):
            libtool("--mode=compile", "--tag=CC",
                    "cc", "-g", "-O",
                    "-c", "blosc_filter.c")
            libtool("--mode=link", "--tag=CC",
                    "cc", "-g", "-O",
                    "-rpath", prefix.lib,
                    "-o", "libblosc_filter.la",
                    "blosc_filter.lo",
                    "-L%s" % spec["c-blosc"].prefix.lib, "-lblosc",
                    "-L%s" % spec["hdf5"].prefix.lib, "-lhdf5")
            _install_shlib("libblosc_filter", ".libs", prefix.lib)

            # Build and install plugin
            # The plugin requires at least HDF5 1.8.11:
            if spec["hdf5"].satisfies("@1.8.11:"):
                libtool("--mode=compile", "--tag=CC",
                        "cc", "-g", "-O",
                        "-c", "blosc_plugin.c")
                libtool("--mode=link", "--tag=CC",
                        "cc", "-g", "-O",
                        "-rpath", prefix.lib,
                        "-o", "libblosc_plugin.la",
                        "blosc_plugin.lo",
                        "-L%s" % prefix.lib, "-lblosc_filter",
                        "-L%s" % spec["c-blosc"].prefix.lib, "-lblosc",
                        "-L%s" % spec["hdf5"].prefix.lib, "-lhdf5")
                _install_shlib("libblosc_plugin", ".libs", prefix.lib)

        self.check_install(spec)

    def check_install(self, spec):
        "Build and run a small program to test the installed HDF5 Blosc plugin"
        print "Checking HDF5-Blosc plugin..."
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""\
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define FILTER_BLOSC 32001 /* Blosc filter ID registered with the HDF group */

int main(int argc, char **argv) {
  herr_t herr;
  hid_t file = H5Fcreate("file.h5", H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
  assert(file >= 0);
  hsize_t dims[3] = {10, 10, 10};
  hid_t space = H5Screate_simple(3, dims, NULL);
  assert(space >= 0);
  hid_t create_proplist = H5Pcreate(H5P_DATASET_CREATE);
  assert(create_proplist >= 0);
  herr = H5Pset_chunk(create_proplist, 3, dims);
  assert(herr >= 0);
  herr = H5Pset_filter(create_proplist, FILTER_BLOSC, H5Z_FLAG_OPTIONAL, 0,
                       NULL);
  assert(herr >= 0);
  htri_t all_filters_avail = H5Pall_filters_avail(create_proplist);
  assert(all_filters_avail > 0);
  hid_t dataset = H5Dcreate(file, "dataset", H5T_NATIVE_DOUBLE, space,
                            H5P_DEFAULT, create_proplist, H5P_DEFAULT);
  assert(dataset >= 0);
  double data[10][10][10];
  for (int k=0; k<10; ++k) {
    for (int j=0; j<10; ++j) {
      for (int i=0; i<10; ++i) {
        data[k][j][i] = 1.0 / (1.0 + i + j + k);
      }
    }
  }
  herr = H5Dwrite(dataset, H5T_NATIVE_DOUBLE, space, space, H5P_DEFAULT,
                  &data[0][0][0]);
  assert(herr >= 0);
  herr = H5Pclose(create_proplist);
  assert(herr >= 0);
  herr = H5Dclose(dataset);
  assert(herr >= 0);
  herr = H5Sclose(space);
  assert(herr >= 0);
  herr = H5Fclose(file);
  assert(herr >= 0);
  printf("Done.\n");
  return 0;
}
"""
            expected = """\
Done.
"""
            with open("check.c", "w") as f:
                f.write(source)
            if "+mpi" in spec["hdf5"]:
                cc = Executable(spec["mpi"].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            # TODO: Automate these path and library settings
            cc("-c", "-I%s" % spec["hdf5"].prefix.include, "check.c")
            cc("-o", "check", "check.o",
               "-L%s" % spec["hdf5"].prefix.lib, "-lhdf5")
            try:
                check = Executable("./check")
                output = check(return_output=True)
            except:
                output = ""
            success = output == expected
            if not success:
                print "Produced output does not match expected output."
                print "Expected output:"
                print "-" * 80
                print expected
                print "-" * 80
                print "Produced output:"
                print "-" * 80
                print output
                print "-" * 80
                print "Environment:"
                env = which("env")
                env()
                raise RuntimeError("HDF5 Blosc plugin check failed")
        shutil.rmtree(checkdir)

    def setup_environment(self, spack_env, run_env):
        spack_env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
        run_env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
        run_env.append_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
