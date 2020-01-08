# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import fnmatch
import shutil


class Adf(Package):
    """Amsterdam Density Functional (ADF) is a program for first-principles
    electronic structure calculations that makes use of density functional
    theory."""

    homepage = "https://www.scm.com/product/adf/"
    version('2017.113', '666ef15d253b74c707dd14da35e7cf283ca20e21e24ed43cb953fb9d1f2f1e15')

    def url_for_version(self, version):
        return "file://{0}/adf/adf{1}.pc64_linux.openmpi.bin.tgz".format(
               os.getcwd(), version)

    # Licensing
    license_required = True
    license_files = ['license.txt']
    license_vars = ['SCMLICENSE']

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', join_path(self.prefix, 'bin'))

        run_env.set('ADFHOME', self.prefix)
        run_env.set('ADFBIN', join_path(self.prefix, 'bin'))
        run_env.set('ADFRESOURCES', join_path(self.prefix, 'atomicdata'))
        run_env.set('SCMLICENSE', join_path(self.prefix, 'license.txt'))
        run_env.set('SCM_TMPDIR', '/tmp')

    def install(self, spec, prefix):
        for filename in os.listdir(self.stage.source_path):
            if os.path.isdir(filename):
                shutil.copytree(filename, join_path(self.prefix, filename))
            elif not fnmatch.fnmatch(filename, "spack-build.*") or \
                    fnmatch.fnmatch(filename, "adf*"):
                shutil.copy(filename, self.prefix)
