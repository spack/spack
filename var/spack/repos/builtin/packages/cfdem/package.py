# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
from spack.util.environment import EnvironmentModifications
import llnl.util.tty as tty


class Cfdem(Package):
    """CFDEM®coupling provides an open source parallel coupled CFD-DEM framework 
    combining the strengths of LIGGGHTS® DEM code and the Open Source CFD package OpenFOAM®(*).
    The CFDEM®coupling toolbox allows to expand standard CFD solvers of OpenFOAM®(*) 
    to include a coupling to the DEM code LIGGGHTS®. 
    """

    homepage = "https://www.cfdem.com/"
    url      = "https://github.com/CFDEMproject/CFDEMcoupling-PUBLIC/archive/3.8.0.tar.gz"
    git      = "https://github.com/CFDEMproject/CFDEMcoupling-PUBLIC.git"

    version('master', branch='master')
    version('3.8.0', sha256='3c90d3178c9667ea84db9507221f65f9efec2aab8d22c51769f8a0c94d813ee4',preferred=True)
    version('3.7.0', sha256='b504b50f930af28639e4cb4073eaf431118a3122f21e8aa470ef05bc58f8976e')
    version('3.6.1', sha256='3f1c9508f2e329e8d2a5812f6b679a6697ceca9b1c35ef2951d984d77b1c873e')
    version('3.6.0', sha256='d70f20aea6acf63f15817f74afa06ed56b3b7a4d049cf980a1b6416aebeeb7c5')
    version('3.5.1', sha256='1661c5b2d6fad1958fdfb5a91c90a2ce0fe5a80ccb1d3188dadd364bbb6bc6ab')
    version('3.5.0', sha256='181799d6c645cfb5c1332f15c233b8486b790fc5290398caaf4973f1be87c20e')
    version('3.4.0', sha256='9070f7aa57d2cd1c7a43d41facbbd008f0b34cdca439bf2a98b90809d86282a0')

   # Dependency information comes from file
   # lagrangian/cfdemParticle/cfdTools/versionInfo.H in source code.
    depends_on('openfoam-org@5.0',when="@master")
    depends_on('openfoam-org@5.0',when="@3.8.1")
    depends_on('openfoam-org@5.0',when="@3.8.0")
    # The openfoam-org package is a modified version of the openfoam-org package.
    # Spack does not have version openfoam-org@3.0.1 on 2021/08/31, 
    # it was added by ourselves
    depends_on('openfoam-org@3.0.1',when="@3.7.0")
    depends_on('openfoam-org@3.0.1',when="@3.6.1")
    depends_on('openfoam-org@3.0.1',when="@3.6.0")
    depends_on('openfoam-org@3.0.1',when="@3.5.1")
    depends_on('openfoam-org@3.0.1',when="@3.5.0")
    depends_on('openfoam-org@3.0.1',when="@3.4.0")
    # The liggghts package is a modified version of the liggghts package.
    # Spack only has version liggghts@3.8.0 on 2021/08/31.
    depends_on('liggghts@3.8.0',when="@master")
    depends_on('liggghts@3.8.0',when="@3.8.1")
    depends_on('liggghts@3.8.0',when="@3.8.0")
    depends_on('liggghts@3.7.0',when="@3.7.0")
    depends_on('liggghts@3.6.0',when="@3.6.1")
    depends_on('liggghts@3.6.0',when="@3.6.0")
    depends_on('liggghts@3.5.0',when="@3.5.1")
    depends_on('liggghts@3.5.0',when="@3.5.0")
    depends_on('liggghts@3.4.0',when="@3.4.0")

    phases = ['edit','build', 'install']

    def setup_build_environment(self, env):

        stage_path = self.stage.source_path

        env.set('CFDEM_PROJECT_DIR', stage_path)
        env.set('CFDEM_bashrc', '{}/src/lagrangian/cfdemParticle/etc/bashrc'.format(stage_path))
        env.set('CFDEM_LIGGGHTS_MAKEFILE_NAME', 'auto')
        env.set('CFDEM_SRC_DIR','{}/src'.format(stage_path))
        env.set('CFDEM_SOLVER_DIR','{}/applications/solvers'.format(stage_path))
        env.set('CFDEM_DOC_DIR','{}/doc'.format(stage_path))
        env.set('CFDEM_UT_DIR','{}/applications/utilities'.format(stage_path))
        env.set('CFDEM_TUT_DIR','{}/tutorials'.format(stage_path))
        env.set('CFDEM_LIGGGHTS_MAKEFILE_POSTIFX','')
        env.set('CFDEM_VERBOSE','false' )
        


        # Some commands or variables such as wmakeLnInclude  are used when cfdem is compiled, 
        # and they are defined in etc/bashrc of other package openfoam-org.
        openfoam_bashrc = join_path(self.spec['openfoam-org'].prefix, 'etc/bashrc')
        try:
            env.extend(EnvironmentModifications.from_sourcing_file(
                openfoam_bashrc, clean=True
            ))
        except Exception as e:
            msg = 'unexpected error when sourcing openfoam-org bashrc [{0}]'
            tty.warn(msg.format(e))

        # After importing openfoam-org's bashrc, the variable WM_PROJECT_VERSION will be set to 5.0,
        # but the format required by cfdem is 5.x
        of_version = '5.x'
        if self.spec['openfoam-org'].version == Version("5.0"):
            of_version = '5.x'
        elif self.spec['openfoam-org'].version == Version("3.0.1"):
            of_version = '3.0.x'

        env.set('WM_PROJECT_VERSION', of_version)

        # liggghts header files and libraries
        liggghts_pre = self.spec['liggghts'].prefix
        env.set('CFDEM_LIGGGHTS_SRC_DIR',  join_path(liggghts_pre, 'src'))
        env.set('CFDEM_LIGGGHTS_LIB_PATH',  join_path(liggghts_pre, 'src'))


    def setup_run_environment(self, env):

        env.set('CFDEM_SRC_DIR','{}/src'.format(self.prefix))
        

        with working_dir('./src/lagrangian/cfdemParticle/etc/'):
            with open('exec_all.sh', 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('\n')
                f.write('echo y >/tmp/autoinput\n')
                f.write('source $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/bashrc < /tmp/autoinput\n')
                f.write('\n')
                f.write('. $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/compileCFDEMcoupling_src.sh\n')
                f.write('echo "#################### finished compileCFDEMcoupling_src ####################"\n')
                f.write('\n')
                f.write('. $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/compileCFDEMcoupling_sol.sh\n')
                f.write('echo "#################### finished compileCFDEMcoupling_sol ####################"\n')
                f.write('\n')
                f.write('. $CFDEM_SRC_DIR/lagrangian/cfdemParticle/etc/compileCFDEMcoupling_uti.sh\n')
                f.write('echo "#################### finished compileCFDEMcoupling_uti ####################"\n')
                f.write('\n')

    def build(self, spec, prefix):

        # run shell script exec_all.sh to compile
        shscript = join_path(os.getcwd(), 'src/lagrangian/cfdemParticle/etc/exec_all.sh')
        set_executable(shscript)
        script = Executable(shscript)
        script()

    def install(self, spec, prefix):
        install_tree('.', prefix)
        install_tree('platforms/linux64GccDPInt32-spack/bin', prefix.bin,symlinks=True)
        install_tree('platforms/linux64GccDPInt32-spack/lib', prefix.lib,symlinks=True)
