# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Gptune(CMakePackage):
    """GPTune is an autotuning framework that relies on multitask and transfer
    learnings to help solve the underlying black-box optimization problem using
    Bayesian optimization methodologies."""

    homepage = "https://gptune.lbl.gov/"
    git      = "https://github.com/gptune/GPTune.git"
    maintainers = ['liuyangzhuan']

    version('master', branch='master')
    variant('app', default=False, description='Build all HPC application examples')
    variant('openmpi', default=True, description='MPI spawning-based interface')

    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('cmake@3.3:', type='build')
    depends_on('jq', type='run')
    depends_on('blas', type='link')
    depends_on('lapack', type='link')
    depends_on('scalapack', type='link')
    depends_on('py-setuptools', type='build')
    depends_on('py-ipyparallel', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-joblib', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-scikit-optimize@master+gptune', type=('build', 'run'))
    depends_on('py-gpy', type=('build', 'run'))
    depends_on('py-lhsmdu', type=('build', 'run'))
    depends_on('py-hpbandster', type=('build', 'run'))
    depends_on('py-opentuner', type=('build', 'run'))
    depends_on('py-ytopt-autotune@1.1.0', type=('build', 'run'))
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-pyaml', type=('build', 'run'))
    depends_on('py-mpi4py@3.0.3:', type=('build', 'run'))
    depends_on('pygmo', type=('build', 'run'))
    depends_on('openturns', type=('build', 'run'))

    depends_on('superlu-dist@develop', when='+app', type=('build', 'run'))
    
    depends_on('openmpi@4:', when='+openmpi')
    conflicts('mpich', when='+openmpi')
    conflicts('spectrum-mpi', when='+openmpi')
    conflicts('cray-mpich', when='+openmpi')

    def cmake_args(self):
        spec = self.spec
        fc_flags = []
        if '%gcc@10:' in spec or self.spec.satisfies('%apple-clang@11:'):
            fc_flags.append('-fallow-argument-mismatch')

        args = [
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
            libs.joined(";"),
            '-DCMAKE_Fortran_FLAGS=' + ''.join(fc_flags),
            '-DBUILD_SHARED_LIBS=ON',
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
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.examples_src_dir)

        if '+app' in spec:
            superludriver = join_path(spec['superlu-dist'].prefix.bin, 'pddrive_spawn')
            op = ['-r', superludriver, '.']
            # copy superlu-dist executables to the correct place
            wd = join_path(test_dir, 'SuperLU_DIST')
            self.run_test('rm', options=['-rf', 'superlu_dist'], work_dir=wd)
            self.run_test('git', options=['clone', 'https://github.com/xiaoyeli/superlu_dist.git'], work_dir=wd)
            self.run_test('mkdir', options=['-p',
                                            'build'], work_dir=wd+'/superlu_dist')
            self.run_test('mkdir', options=['-p', 'EXAMPLE'],
                            work_dir=wd+'/superlu_dist/build')
            self.run_test('cp', options=op, work_dir=wd+'/superlu_dist/build/EXAMPLE')

        wd = self.test_suite.current_test_cache_dir
        cdir = join_path(self.prefix, 'gptuneclcm')
        self.run_test('cp', options=['-r', cdir, '.'], work_dir=wd)
        self.run_test('rm', options=['-rf', 'build'], work_dir=wd)
        self.run_test('mv', options=['gptuneclcm', 'build'], work_dir=wd)

        with open('{0}/run_env.sh'.format(wd), 'w') as envfile:
            envfile.write('if [[ $NERSC_HOST = "cori" ]]; then\n')
            envfile.write('    export machine=cori\n')
            envfile.write('elif [[ $(uname -s) = "Darwin" ]]; then\n')
            envfile.write('    export machine=mac\n')
            envfile.write('elif [[ $(dnsdomainname) = ' +
                            '"summit.olcf.ornl.gov" ]]; then\n')
            envfile.write('    export machine=summit\n')
            envfile.write('elif [[ $(cat /etc/os-release | grep "PRETTY_NAME") ==' +
                            ' *"Ubuntu"* || $(cat /etc/os-release | grep' +
                            ' "PRETTY_NAME") == *"Debian"* ]]; then\n')
            envfile.write('    export machine=unknownlinux\n')
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
            if '+openmpi' in spec:
                apps = ['GPTune-Demo', 'SuperLU_DIST', 'SuperLU_DIST_RCI',
                        'Scalapack-PDGEQRF', 'Scalapack-PDGEQRF_RCI']                
            else:
                apps = ['SuperLU_DIST_RCI', 'Scalapack-PDGEQRF_RCI'] 
        else:
            if '+openmpi' in spec:
                apps = ['GPTune-Demo', 'Scalapack-PDGEQRF', 'Scalapack-PDGEQRF_RCI']
            else:
                apps = ['Scalapack-PDGEQRF_RCI']

        for app in apps:
            wd = join_path(test_dir, app)
            self.run_test('bash', options=['run_examples.sh'], work_dir=wd,
                            purpose='gptune smoke test for {0}'.format(app))
