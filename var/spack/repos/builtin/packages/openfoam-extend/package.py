from spack import *
from spack.environment import *

import multiprocessing
import subprocess
import re
import os


class OpenfoamExtend(Package):
    """OpenFOAM-extend or foam-extend"""

    version('3.2', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.2')
    version('3.1', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.1')
    version('3.0', git='http://git.code.sf.net/p/foam-extend/foam-extend-3.0')

    variant('paraview', default=False, description='Enable ParaFOAM')
    variant('scotch', default=True, description='Activate Scotch as a possible decomposition library')
    variant('ptscotch', default=True, description='Activate PT-Scotch as a possible decomposition library')
    variant('metis', default=True, description='Activate Metis as a possible decomposition library')
    variant('parmetis', default=True, description='Activate Parmetis as a possible decomposition library')
    variant('parmgridgen', default=True, description='Activate Parmgridgen support')

    supported_compilers = {'clang': 'Clang', 'gcc': 'Gcc', 'intel': 'Icc'}

    depends_on('mpi')
    depends_on('cmake')
    depends_on('python')
    depends_on('flex@:2.5.99')
    depends_on('bison')
    depends_on('m4')
    depends_on('hwloc')
    depends_on('zlib')

    depends_on('scotch ~ metis', when='~ptscotch+scotch')
    depends_on('scotch ~ metis + mpi', when='+ptscotch')
    depends_on('metis@5:', when='+metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('parmgridgen', when='+parmgridgen')

    depends_on('paraview', when='+paraview')
    depends_on('qt@:4', when='+paraview')

    def _get_env(self, command):
        variable_set = re.compile(r'(.+?)=(.*)')
        proc = subprocess.Popen(['bash', '-c', command],
                                stdout=subprocess.PIPE)
        env = {}
        for line in proc.stdout:
            match_grp = variable_set.match(line)
            if match_grp:
                env[match_grp.group(1)] = match_grp.group(2)
        return env

    def set_arch(self):
        (sysname, nodename, release, version, machine) = os.uname()

        if self.compiler.name not in self.supported_compilers:
            raise RuntimeError('{0} is not a supported compiler \
            to compile OpenFOAM'.format(self.compiler.name))

        foam_compiler = self.supported_compilers[self.compiler.name]
        if sysname == 'Linux':
            arch = 'linux'
            if foam_compiler == 'Clang':
                raise RuntimeError('OS, compiler combinaison not\
                supported ({0} {1})'.format(sysname, foam_compiler))
        elif sysname == 'Darwin':
            if machine == 'x86_64':
                arch = 'darwinIntel'
            if foam_compiler == 'Icc':
                raise RuntimeError('OS, compiler combinaison not\
                supported ({0} {1})'.format(sysname, foam_compiler))
        else:
            raise RuntimeError('{0} {1} is not a \
            supported architecture'.format(sysname, machine))

        return (arch, foam_compiler)

    def get_openfoam_environment(self, env_openfoam):
        env_before = self._get_env('env')

        with working_dir(self.stage.source_path):
            env_after = self._get_env('source etc/bashrc && env')

        if 'PATH' in env_after:
            del env_after['PATH']

        if 'LD_LIBRARY_PATH' in env_after:
            del env_after['LD_LIBRARY_PATH']

        for key, value in env_after.iteritems():
            if key not in env_before or not value == env_before[key]:
                env_openfoam.set(key, value)

    def patch(self):
        if '+parmgridgen' in self.spec:
            filter_file(r'-lIMlib -lMGridGen',
                        r'-limlib -lmgrid',
                        'src/dbns/Make/options')
            filter_file(r'-lMGridGen',
                        r'-lmgrid',
                        'src/fvAgglomerationMethods/MGridGenGamgAgglomeration/Make/options')

        (arch, foam_compiler) = self.set_arch()

        prefs_dict = {
            'compilerInstall': 'System',
            'WM_COMPILER': foam_compiler,
            'WM_ARCH_OPTION': '64',
            'WM_PRECISION_OPTION': 'DP',
            'WM_COMPILE_OPTION': 'SPACKOpt',
            'WM_MPLIB': 'SPACK',

            'CMAKE_DIR': self.spec['cmake'].prefix,
            'CMAKE_BIN_DIR': self.spec['cmake'].prefix.bin,
            'PYTHON_DIR': self.spec['python'].prefix,
            'PYTHON_BIN_DIR': self.spec['python'].prefix.bin,

            'FLEX_SYSTEM': 1,
            'FLEX_DIR': self.spec['flex'].prefix,

            'BISON_SYSTEM': 1,
            'BISON_DIR': self.spec['flex'].prefix,

            'M4_SYSTEM': 1,
            'M4_DIR': self.spec['m4'].prefix,

            'ZLIB_SYSTEM': 1,
            'ZLIB_DIR': self.spec['zlib'].prefix,

            'HWLOC_SYSTEM': 1,
            'HWLOC_DIR': self.spec['hwloc'].prefix,
            'HWLOC_BIN_DIR': self.spec['hwloc'].prefix.bin,
        }

        if '+scotch' in self.spec or '+ptscotch' in self.spec:
            prefs_dict['SCOTCH_SYSTEM'] = 1
            prefs_dict['SCOTCH_DIR'] = self.spec['scotch'].prefix
            prefs_dict['SCOTCH_BIN_DIR'] = self.spec['scotch'].prefix.bin
            prefs_dict['SCOTCH_LIB_DIR'] = self.spec['scotch'].prefix.lib
            prefs_dict['SCOTCH_INCLUDE_DIR'] = \
                self.spec['scotch'].prefix.include

        if '+metis' in self.spec:
            prefs_dict['METIS_SYSTEM'] = 1
            prefs_dict['METIS_DIR'] = self.spec['metis'].prefix
            prefs_dict['METIS_BIN_DIR'] = self.spec['metis'].prefix.bin
            prefs_dict['METIS_LIB_DIR'] = self.spec['metis'].prefix.lib
            prefs_dict['METIS_INCLUDE_DIR'] = self.spec['metis'].prefix.include

        if '+parmetis' in self.spec:
            prefs_dict['PARMETIS_SYSTEM'] = 1
            prefs_dict['PARMETIS_DIR'] = self.spec['parmetis'].prefix
            prefs_dict['PARMETIS_BIN_DIR'] = self.spec['parmetis'].prefix.bin
            prefs_dict['PARMETIS_LIB_DIR'] = self.spec['parmetis'].prefix.lib
            prefs_dict['PARMETIS_INCLUDE_DIR'] = \
                self.spec['parmetis'].prefix.include

        if '+parmgridgen' in self.spec:
            prefs_dict['PARMGRIDGEN_SYSTEM'] = 1
            prefs_dict['PARMGRIDGEN_DIR'] = self.spec['parmgridgen'].prefix
            prefs_dict['PARMGRIDGEN_BIN_DIR'] = \
                self.spec['parmgridgen'].prefix.bin
            prefs_dict['PARMGRIDGEN_LIB_DIR'] = \
                self.spec['parmgridgen'].prefix.lib
            prefs_dict['PARMGRIDGEN_INCLUDE_DIR'] = \
                self.spec['parmgridgen'].prefix.include

        if '+paraview' in self.spec:
            prefs_dict['PARAVIEW_SYSTEM'] = 1
            prefs_dict['PARAVIEW_DIR'] = self.spec['paraview'].prefix,
            prefs_dict['PARAVIEW_BIN_DIR'] = self.spec['paraview'].prefix.bin,
            prefs_dict['QT_SYSTEM'] = 1
            prefs_dict['QT_DIR'] = self.spec['qt'].prefix,
            prefs_dict['QT_BIN_DIR'] = self.spec['qt'].prefix.bin,

        with working_dir('.'):
            with open("etc/prefs.sh", "w") as fh:
                for key in sorted(prefs_dict):
                    fh.write('export {0}={1}\n'.format(key, prefs_dict[key]))

            with open("etc/prefs.csh", "w") as fh:
                for key in sorted(prefs_dict):
                    fh.write('setenv {0}={1}\n'.format(key, prefs_dict[key]))

        mpi_info = [
            'PFLAGS = -DOMPI_SKIP_MPICXX -DMPICH_IGNORE_CXX_SEEK',
            'PINC = -I{0}'.format(self.spec['mpi'].prefix.include),
            'PLIBS = -L{0} -lmpi'.format(self.spec['mpi'].prefix.lib)
        ]

        arch_path = ''.join([arch, prefs_dict['WM_ARCH_OPTION'],
                             foam_compiler])
        option_path = ''.join([arch_path,
                               prefs_dict['WM_PRECISION_OPTION'],
                               prefs_dict['WM_COMPILE_OPTION']])
        rule_path = join_path("wmake", "rules", arch_path)
        build_path = join_path(self.stage.source_path, 'lib', option_path)
        install_path = \
            join_path(self.prefix,
                      'foam-extend-{0}'.format(self.version.up_to(2)),
                      option_path)

        rpaths_foam = ' '.join([
            '{0}{1}'.format(self.compiler.cxx_rpath_arg,
                            install_path),
            '{0}{1}'.format(self.compiler.cxx_rpath_arg,
                            build_path)
        ])

        compiler_flags = {
            'DBUG': rpaths_foam,
            'OPT': '-O3',
        }

        with working_dir(rule_path):
            with open('mplibSPACK', "w") as fh:
                fh.write('\n'.join(mpi_info))

            for comp in ['c', 'c++']:
                with open('{0}SPACKOpt'.format(comp), "w") as fh:
                    for key, val in compiler_flags.iteritems():
                        fh.write('{0}{1} = {2}\n'.format(comp, key, val))

    def setup_environment(self, spack_env, run_env):
        with working_dir(self.stage.path):
            spack_env.set('FOAM_INST_DIR', os.path.abspath('.'))

        (arch, foam_compiler) = self.set_arch()

        run_env.set('FOAM_INST_DIR', self.prefix)

    def install(self, spec, prefix):
        self.patch()

        env_openfoam = EnvironmentModifications()
        self.get_openfoam_environment(env_openfoam)
        env_openfoam.apply_modifications()

        if self.parallel:
            os.environ['WM_NCOMPPROCS'] = str(self.make_jobs) \
                if self.make_jobs else str(multiprocessing.cpu_count())

        # for key in sorted(os.environ):
        #     print("{0} = {1}".format(key, os.environ[key]))

        allwmake = Executable('./Allwmake')
        allwmake()

        install_path = \
            join_path(self.prefix,
                      'foam-extend-{0}'.format(self.version.up_to(2)))

        if '+source' in spec:
            install_tree('src', join_path(install_path, 'src'))

        install_tree('lib', join_path(install_path, 'lib'))
        install_tree('bin', join_path(install_path, 'bin'))
        install_tree('applications', join_path(install_path, 'applications'))
        install_tree('etc', join_path(install_path, 'etc'))
        install_tree('wmake', join_path(install_path, 'wmake'))
