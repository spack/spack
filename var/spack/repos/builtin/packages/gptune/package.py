# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Gptune(CMakePackage):
    """GPTune is an autotuning framework that relies on multitask and transfer
    learnings to help solve the underlying black-box optimization problem using
    Bayesian optimization methodologies."""

    homepage = "https://gptune.lbl.gov/"
    git      = "https://github.com/gptune/GPTune.git"

    version('master', branch='master')

    variant('app', default=False, description='Build all HPC application examples')

    depends_on('mpi')
    depends_on('cmake@3.3:')
    depends_on('jq')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')
    depends_on('py-setuptools')
    depends_on('py-ipyparallel')
    depends_on('py-pip')
    depends_on('py-numpy')
    depends_on('py-pandas')
    depends_on('py-joblib')
    depends_on('py-scikit-learn')
    depends_on('py-matplotlib')
    depends_on('py-pyyaml')
    depends_on('py-scikit-optimize@master+gptune')
    depends_on('py-gpy')
    depends_on('py-lhsmdu')
    depends_on('py-hpbandster')
    depends_on('py-opentuner')
    depends_on('py-autotune')
    depends_on('py-filelock')
    depends_on('py-requests')
    depends_on('py-cython')
    depends_on('py-pyaml')
    depends_on('py-mpi4py@3.0.3:')
    depends_on('pygmo')

    depends_on('superlu-dist@develop', when='+app')

    conflicts('openmpi@:4.0.0')

    def cmake_args(self):
        spec = self.spec
        fc_flags = []
        if '%gcc@10:' in spec:
            fc_flags.append('-fallow-argument-mismatch')
        if self.spec.satisfies('%apple-clang@11:'):
            fc_flags.append('-fallow-argument-mismatch')
        if self.spec.satisfies('%clang@11:'):
            fc_flags.append('-fallow-argument-mismatch')

        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            '-DCMAKE_INSTALL_PREFIX=%s' % self.prefix,
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
            libs.joined(";"),
            '-DCMAKE_Fortran_FLAGS=' + ''.join(fc_flags),
            '-DBUILD_SHARED_LIBS=ON',
            '-DCMAKE_BUILD_TYPE=Release',
        ]

        return args

    examples_src_dir = 'examples'
    src_dir = 'GPTune'
    nodes = 1
    cores = 4

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir, self.src_dir])

    def test(self):
        spec = self.spec
        comp_name = self.compiler.name
        comp_version = str(self.compiler.version).replace('.', ',')
        test_dir = join_path(self.install_test_root, self.examples_src_dir)

        if '+app' in spec:
            superludriver = join_path(spec['superlu-dist'].prefix.bin, 'pddrive_spawn')
            op = ['-r', superludriver, '.']
            # copy superlu-dist executables to the correct place
            with working_dir(join_path(test_dir, 'SuperLU_DIST'), create=False):
                self.run_test('rm', options=['-rf', 'superlu_dist'], work_dir='.')
                self.run_test('git', options=['clone', 'https://github.com/xiaoyeli/superlu_dist.git'], work_dir='.')
                self.run_test('mkdir', options=['-p',
                                                'build'], work_dir='./superlu_dist')
                self.run_test('mkdir', options=['-p', 'EXAMPLE'],
                              work_dir='./superlu_dist/build')
                self.run_test('cp', options=op, work_dir='./superlu_dist/build/EXAMPLE')

        setupenv = '. $PWD/../../../../../../../share/spack/setup-env.sh\n'
        with working_dir(self.install_test_root, create=False):
            cdir = join_path(self.prefix, 'gptuneclcm')
            self.run_test('cp', options=['-r', cdir, '.'], work_dir='.')
            self.run_test('rm', options=['-rf', 'build'], work_dir='.')
            self.run_test('mv', options=['gptuneclcm', 'build'], work_dir='.')

            with open('{0}/run_env.sh'.format(self.install_test_root), 'w') as envfile:
                envfile.write(setupenv)
                envfile.write('spack load --only dependencies gptune\n')
                envfile.write('spack load python\n')
                envfile.write('spack load py-pip\n')
                envfile.write('pip install urllib3\n')
                envfile.write('pip install openturns\n')
                envfile.write('pip install cloudpickle\n')
                envfile.write('pip install configspace\n')
                envfile.write('pip install Pyro4\n')
                envfile.write('pip install statsmodels\n')
                envfile.write('if [[ $(hostname -s) = "tr4-workstation" ]]; then\n')
                envfile.write('    export machine=tr4-workstation\n')
                envfile.write('elif [[ $NERSC_HOST = "cori" ]]; then\n')
                envfile.write('    export machine=cori\n')
                envfile.write('elif [[ $(uname -s) = "Darwin" ]]; then\n')
                envfile.write('    export machine=mac\n')
                envfile.write('elif [[ $(dnsdomainname) = ' +
                              '"summit.olcf.ornl.gov" ]]; then\n')
                envfile.write('    export machine=summit\n')
                envfile.write('elif [[ $(cat /etc/os-release | grep "PRETTY_NAME") ==' +
                              ' *"Ubuntu"* || $(cat /etc/os-release | grep' +
                              ' "PRETTY_NAME") == *"Debian"* ]]; then\n')
                envfile.write('    export machine=cleanlinux\n')
                envfile.write('fi\n')
                envfile.write('export GPTUNEROOT=$PWD\n')
                envfile.write('export MPIRUN={0}\n'.format
                              (which(spec['mpi'].prefix.bin + '/mpirun')))
                envfile.write('export proc=$(spack arch)\n')
                envfile.write('export mpi={0}\n'.format(spec['mpi'].name))
                envfile.write('export compiler={0}\n'.format(comp_name))
                envfile.write('export nodes={0} \n'.format(self.nodes))
                envfile.write('export cores={0} \n'.format(self.cores))
                envfile.write('export ModuleEnv=$machine-$proc-$mpi-$compiler \n')
                envfile.write('software_json=$(echo ",\\\"software_configuration\\\":' +
                              '{\\\"' + spec['blas'].name +
                              '\\\":{\\\"version_split\\\":' +
                              ' [' + str(spec['blas'].versions).replace('.', ',') +
                              ']},\\\"' + spec['mpi'].name +
                              '\\\":{\\\"version_split\\\": [' +
                              str(spec['mpi'].versions).replace('.', ',') + ']},\\\"' +
                              spec['scalapack'].name +
                              '\\\":{\\\"version_split\\\": [' +
                              str(spec['scalapack'].versions).replace('.', ',') +
                              ']},\\\"' +
                              str(comp_name) + '\\\":{\\\"version_split\\\": [' +
                              str(comp_version) + ']}}") \n')
                envfile.write('loadable_software_json=$(echo ",\\\"loadable_software_' +
                              'configurations\\\":{\\\"' + spec['blas'].name +
                              '\\\":{\\\"version_split\\\": [' +
                              str(spec['blas'].versions).replace('.', ',') +
                              ']},\\\"' + spec['mpi'].name +
                              '\\\":{\\\"version_split\\\": [' +
                              str(spec['mpi'].versions).replace('.', ',') + ']},\\\"' +
                              spec['scalapack'].name +
                              '\\\":{\\\"version_split\\\": [' +
                              str(spec['scalapack'].versions).replace('.', ',') +
                              ']},\\\"' + str(comp_name) +
                              '\\\":{\\\"version_split\\\": ['
                              + str(comp_version) + ']}}") \n')
                envfile.write('machine_json=$(echo ",\\\"machine_configuration\\\":' +
                              '{\\\"machine_name\\\":\\\"$machine\\\",\\\"$proc\\\":' +
                              '{\\\"nodes\\\":$nodes,\\\"cores\\\":$cores}}") \n')
                envfile.write('loadable_machine_json=$(echo ",\\\"loadable_machine_' +
                              'configurations\\\":{\\\"$machine\\\":{\\\"$proc\\\":' +
                              '{\\\"nodes\\\":$nodes,\\\"cores\\\":$cores}}}") \n')

        if '+app' in spec:
            apps = ['GPTune-Demo', 'SuperLU_DIST', 'SuperLU_DIST_RCI',
                    'Scalapack-PDGEQRF', 'Scalapack-PDGEQRF_RCI']
        else:
            apps = ['GPTune-Demo', 'Scalapack-PDGEQRF', 'Scalapack-PDGEQRF_RCI']

        for app in apps:
            with working_dir(join_path(test_dir, app), create=False):
                # PDGEQRF with GPTune
                self.run_test('bash', options=['run_examples.sh'], work_dir='.',
                              purpose='gptune smoke test for {0}'.format(app))
