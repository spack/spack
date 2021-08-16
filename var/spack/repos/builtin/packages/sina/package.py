import os

from spack import *


class Sina(CachedCMakePackage):
    """Sina C++ Library"""

    homepage = 'https://github.com/LLNL/Sina'
    url = 'https://github.com/LLNL/Sina/releases/download/v1.10.0/sina-cpp-1.10.0.tar.gz'

    version('develop', git='git@github.com:LLNL/Sina.git',
            submodules=True, branch='develop')
    version('1.10.0', sha256='b34379ce8cc5eca5a0f16893053fac75be14c2109d1beed4c6d48e11f9b281c7')

    variant('docs', default=False,
            description='Allow generating documentation')
    variant('adiak', default=False,
            description='Create interface for calling Sina through Adiak')
    # Availability of the adiak version with optional mpi varies
    variant('adiak-no-mpi', default=False,
            description='Create interface for calling Sina through Adiak')
    variant('test', default=False,
            description='Build tests')

    depends_on('cmake@3.8.0:', type='build')
    depends_on('adiak', when='+adiak')
    depends_on('mpi', when='+adiak')
    depends_on('adiak ~mpi', when='+adiak-no-mpi')
    depends_on('doxygen', type='build', when='+docs')
    depends_on('conduit ~python ~mpi ~hdf5 ~silo ~shared ~test ~hdf5_compat')

    def configure_args(self):
        spec = self.spec if self.spec is not None else ''
        return [
            '-DSINA_BUILD_ADIAK_BINDINGS={0}'.format('YES' if '+adiak' in spec or '+adiak-no-mpi' in spec else 'NO'),
            '-DSINA_BUILD_TESTS={0}'.format('YES' if '+test' in spec else 'NO'),
            '-DSINA_BUILD_DOCS={0}'.format('YES' if '+docs' in spec else 'NO'),
        ]

    def initconfig_package_entries(self):
        entries = [
           '#' + 78 * '-',
           '# Library Dependencies',
           '#' + 78 * '-'
        ]
        path_replacements = {}

        # Try to find the common prefix of the TPL directory, including the compiler
        # If found, we will use this in the TPL paths
        compiler_str = str(self.spec.compiler).replace('@','-')
        prefix_paths = prefix.split(compiler_str)
        if len(prefix_paths) == 2:
            tpl_root = os.path.join( prefix_paths[0], compiler_str )
            path_replacements[tpl_root] = '${TPL_ROOT}'
            entries.append(cmake_cache_path('TPL_ROOT', tpl_root))

        conduit_dir = get_spec_path(self.spec, 'conduit', path_replacements)
        entries.append(cmake_cache_path(
            'Conduit_DIR', '{}/lib/cmake/conduit'.format(conduit_dir)))

        use_adiak = '+adiak' in self.spec or '+adiak-no-mpi' in self.spec
        entries.append(cmake_cache_option('SINA_BUILD_ADIAK_BINDINGS', use_adiak))
        if use_adiak:
            adiak_dir = get_spec_path(self.spec, 'adiak', path_replacements)
            entries.append(cmake_cache_path(
                'adiak_DIR', '{}/lib/cmake/adiak/'.format(adiak_dir)))

        entries.append('#' + 78 * '-')
        entries.append('# Devtools')
        entries.append('#' + 78 * '-')

        build_tests = '+test' in self.spec
        entries.append(cmake_cache_option('SINA_BUILD_TESTS', build_tests))

        build_docs = '+docs' in self.spec
        entries.append(cmake_cache_option('SINA_BUILD_DOCS', build_docs))
        if build_docs:
            doxygen_bin_dir = get_spec_path(self.spec, 'doxygen', path_replacements, use_bin=True)
            entries.append(cmake_cache_path('DOXYGEN_EXECUTABLE', os.path.join(doxygen_bin_dir, 'doxygen')))

        return entries


def get_spec_path(spec, package_name, path_replacements = {}, use_bin = False) :
    """Extracts the prefix path for the given spack package
       path_replacements is a dictionary with string replacements for the path.
    """

    if not use_bin:
        path = spec[package_name].prefix
    else:
        path = spec[package_name].prefix.bin

    path = os.path.realpath(path)

    for key in path_replacements:
        path = path.replace(key, path_replacements[key])

    return path

