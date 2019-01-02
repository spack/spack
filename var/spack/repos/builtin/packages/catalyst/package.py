# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import subprocess
import llnl.util.tty as tty


class Catalyst(CMakePackage):
    """Catalyst is an in situ use case library, with an adaptable application
    programming interface (API), that orchestrates the alliance between
    simulation and analysis and/or visualization tasks."""

    homepage = 'http://www.paraview.org'
    url      = "http://www.paraview.org/files/v5.5/ParaView-v5.5.2.tar.gz"
    _urlfmt_gz = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.gz'
    _urlfmt_xz = 'http://www.paraview.org/files/v{0}/ParaView-v{1}{2}.tar.xz'

    version('5.5.2', '7eb93c31a1e5deb7098c3b4275e53a4a')
    version('5.5.1', 'a7d92a45837b67c3371006cc45163277')
    version('5.5.0', 'a8f2f41edadffdcc89b37fdc9aa7f005')
    version('5.4.1', '4030c70477ec5a85aa72d6fc86a30753')
    version('5.4.0', 'b92847605bac9036414b644f33cb7163')
    version('5.3.0', '68fbbbe733aa607ec13d1db1ab5eba71')
    version('5.2.0', '4570d1a2a183026adb65b73c7125b8b0')
    version('5.1.2', '44fb32fc8988fcdfbc216c9e40c3e925')
    version('5.0.1', 'fdf206113369746e2276b95b257d2c9b')
    version('4.4.0', 'fa1569857dd680ebb4d7ff89c2227378')

    variant('python', default=False, description='Enable Python support')
    variant('essentials', default=False, description='Enable Essentials support')
    variant('extras', default=False, description='Enable Extras support')
    variant('rendering', default=False, description='Enable VTK Rendering support')
    variant('osmesa', default=True, description='Use offscreen rendering')

    depends_on('git', type='build')
    depends_on('mpi')
    depends_on('python@2:2.8', when='+python', type=("build", "link", "run"))
    depends_on('python', when='~python', type=("build"))
    depends_on('mesa', when='+rendering')
    depends_on('libx11', when='+rendering')
    depends_on('libxt', when='+rendering')
    depends_on('cmake@3.3:', type='build')

    @when('@5.5.0:5.5.2')
    def patch(self):
        """Apply the patch (it should be fixed in Paraview 5.6)
        at the package dir to the source code in
        root_cmakelists_dir."""
        patch_name = 'vtkm-catalyst-pv551.patch'
        patch = which("patch", required=True)
        with working_dir(self.root_cmakelists_dir):
            patch('-s', '-p', '1', '-i',
                  join_path(self.package_dir, patch_name),
                  "-d", '.')

    def url_for_version(self, version):
        """Handle ParaView version-based custom URLs."""
        if version < Version('5.1.0'):
            return self._urlfmt_gz.format(version.up_to(2), version, '-source')
        elif version < Version('5.6.0'):
            return self._urlfmt_gz.format(version.up_to(2), version, '')
        else:
            return self._urlfmt_xz.format(version.up_to(2), version, '')

    @property
    def paraview_subdir(self):
        """The paraview subdirectory name as paraview-major.minor"""
        return 'paraview-{0}'.format(self.spec.version.up_to(2))

    @property
    def editions(self):
        """Transcribe spack variants into names of Catalyst Editions"""
        selected = ['Base']  # Always required

        if '+python' in self.spec:
            selected.append('Enable-Python')

        if '+essentials' in self.spec:
            selected.append('Essentials')

        if '+extras' in self.spec:
            selected.append('Extras')

        if '+rendering' in self.spec:
            selected.append('Rendering-Base')

        return selected

    def do_stage(self, mirror_only=False):
        """Unpacks and expands the fetched tarball.
        Then, generate the catalyst source files."""
        super(Catalyst, self).do_stage(mirror_only)

        # extract the catalyst part
        paraview_dir = os.path.join(self.stage.path,
                                    'ParaView-v' + str(self.version))
        catalyst_script = os.path.join(paraview_dir, 'Catalyst', 'catalyze.py')
        editions_dir = os.path.join(paraview_dir, 'Catalyst', 'Editions')
        catalyst_source_dir = os.path.abspath(self.root_cmakelists_dir)

        command = ['python', catalyst_script,
                   '-r', paraview_dir,
                   '-o', catalyst_source_dir]

        for edition in self.editions:
            command.extend(['-i', os.path.join(editions_dir, edition)])

        if not os.path.isdir(catalyst_source_dir):
            os.mkdir(catalyst_source_dir)
            subprocess.check_call(command)
            tty.msg("Generated catalyst source in %s" % self.stage.path)
        else:
            tty.msg("Already generated %s in %s" % (self.name,
                                                    self.stage.path))

    def setup_environment(self, spack_env, run_env):
        # paraview 5.5 and later
        # - cmake under lib/cmake/paraview-5.5
        # - libs  under lib
        # - python bits under lib/python2.8/site-packages
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        if self.spec.version <= Version('5.4.1'):
            lib_dir = join_path(lib_dir, paraview_subdir)
        run_env.set('ParaView_DIR', self.prefix)
        run_env.prepend_path('LIBRARY_PATH', lib_dir)
        run_env.prepend_path('LD_LIBRARY_PATH', lib_dir)

        if '+python' in self.spec:
            python_version = self.spec['python'].version.up_to(2)
            run_env.prepend_path('PYTHONPATH', join_path(lib_dir,
                                 'python{0}'.format(python_version),
                                 'site-packages'))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('ParaView_DIR', self.prefix)

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return os.path.join(self.stage.path, 'Catalyst-v' + str(self.version))

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """
        return join_path(os.path.abspath(self.root_cmakelists_dir),
                         'spack-build')

    def cmake_args(self):
        """Populate cmake arguments for Catalyst."""
        spec = self.spec

        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        def nvariant_bool(feature):
            """Negated ternary for spec variant to OFF/ON string"""
            return variant_bool(feature, on='OFF', off='ON')

        cmake_args = [
            '-DPARAVIEW_GIT_DESCRIBE=v%s' % str(self.version),
            '-DVTK_USE_SYSTEM_EXPAT:BOOL=ON',
            '-DVTK_USE_X:BOOL=%s' % nvariant_bool('+osmesa'),
            '-DVTK_USE_OFFSCREEN:BOOL=%s' % variant_bool('+osmesa'),
            '-DVTK_OPENGL_HAS_OSMESA:BOOL=%s' % variant_bool('+osmesa')
        ]
        return cmake_args

    def cmake(self, spec, prefix):
        """Runs ``cmake`` in the build directory through the cmake.sh script"""
        cmake_script_path = os.path.join(
            os.path.abspath(self.root_cmakelists_dir),
            'cmake.sh')
        with working_dir(self.build_directory, create=True):
            subprocess.check_call([cmake_script_path,
                                   os.path.abspath(self.root_cmakelists_dir)] +
                                  self.cmake_args() + self.std_cmake_args)
