# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack import *


class Mesa(MesonPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "https://www.mesa3d.org"
    maintainers = ['chuckatkins', 'v-dobrev']

    git = "https://gitlab.freedesktop.org/mesa/mesa.git"
    url = "https://archive.mesa3d.org/mesa-20.2.1.tar.xz"

    version('master', tag='master')
    # Note: If v22.x or greater is added please leave 21.3.8 as preferred.  The swr
    # multithreaded cpu driver was dropped 22.x and is currently necessary to get
    # reasonable rendering performance on HPC OpenGL workloads.
    # See https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/11264
    version('21.3.8', sha256='e70d273bdc53a4e931871bb5550ba3900e6a3deab2fff64184107c33e92d9da7', preferred=True)
    version('21.3.7', sha256='b4fa9db7aa61bf209ef0b40bef83080999d86ad98df8b8b4fada7c128a1efc3d')
    version('21.3.1', sha256='2b0dc2540cb192525741d00f706dbc4586349185dafc65729c7fda0800cc474d')
    version('21.2.6', sha256='1e7e22d93c6e8859fa044b1121119d26b2e67e4184b92ebb81c66497dc80c954')
    version('21.2.5', sha256='8e49585fb760d973723dab6435d0c86f7849b8305b1e6d99f475138d896bacbb')
    version('21.2.4', sha256='fe6ede82d1ac02339da3c2ec1820a379641902fd351a52cc01153f76eff85b44')
    version('21.2.3', sha256='7245284a159d2484770e1835a673e79e4322a9ddf43b17859668244946db7174')
    version('21.2.1', sha256='2c65e6710b419b67456a48beefd0be827b32db416772e0e363d5f7d54dc01787')
    version('21.0.3', sha256='565c6f4bd2d5747b919454fc1d439963024fc78ca56fd05158c3b2cde2f6912b')
    version('21.0.0', sha256='e6204e98e6a8d77cf9dc5d34f99dd8e3ef7144f3601c808ca0dd26ba522e0d84')
    version('20.3.4', sha256='dc21a987ec1ff45b278fe4b1419b1719f1968debbb80221480e44180849b4084')
    version('20.2.1', sha256='d1a46d9a3f291bc0e0374600bdcb59844fa3eafaa50398e472a36fc65fd0244a')

    depends_on('meson@0.52:', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('bison', type='build')
    depends_on('cmake', type='build')
    depends_on('flex', type='build')
    depends_on('gettext', type='build')
    depends_on('python@3:', type='build')
    depends_on('py-mako@0.8.0:', type='build')
    depends_on('unwind')
    depends_on('expat')
    depends_on('zlib@1.2.3:')

    # Override the build type variant so we can default to release
    variant('buildtype', default='release',
            description='Meson build type',
            values=('plain', 'debug', 'debugoptimized', 'release', 'minsize'))

    # Internal options
    variant('llvm', default=True, description="Enable LLVM.")

    # when clauses:
    #   +llvm - swr requires llvm
    #   buildtype=release - swr has known assert failures in debug that can be ignored
    #   @:21  - swr was removed in 22.0; see note above
    variant(
        'swr',
        values=spack.variant.DisjointSetsOfValues(
            ('none',), ('auto',), ('avx', 'avx2', 'knl', 'skx',),
        )
        .with_non_feature_values('auto')
        .with_non_feature_values('none')
        .with_default('auto'),
        when='+llvm buildtype=release @:21',
        description="Enable the SWR driver.",
    )

    # Front ends
    variant('osmesa', default=True, description="Enable the OSMesa frontend.")

    is_linux = sys.platform.startswith('linux')
    variant('glx', default=is_linux, description="Enable the GLX frontend.")

    # TODO: effectively deal with EGL.  The implications of this have not been
    # worked through yet
    # variant('egl', default=False, description="Enable the EGL frontend.")

    # TODO: Effectively deal with hardware drivers
    # The implication of this is enabling DRI, among other things, and
    # needing to check which llvm targets were built (ptx or amdgpu, etc.)

    # Back ends
    variant('opengl', default=True, description="Enable full OpenGL support.")
    variant('opengles', default=False, description="Enable OpenGL ES support.")

    # Provides
    provides('gl@4.5',  when='+opengl')
    provides('glx@1.4', when='+glx')
    # provides('egl@1.5', when='+egl')
    provides('osmesa', when='+osmesa')

    # Variant dependencies
    depends_on('libllvm@6:', when='+llvm')
    depends_on('libllvm@:13', when='@:21 +llvm')
    depends_on('libx11',  when='+glx')
    depends_on('libxcb',  when='+glx')
    depends_on('libxext', when='+glx')
    depends_on('libxt',  when='+glx')
    depends_on('xrandr', when='+glx')
    depends_on('glproto@1.4.14:', when='+glx')

    # version specific issue
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=96130
    conflicts('%gcc@10.1.0', msg='GCC 10.1.0 has a bug')

    # Require at least 1 front-end
    # TODO: Add egl to this conflict once made available
    conflicts('~osmesa ~glx')

    # Require at least 1 back-end
    # TODO: Add vulkan to this conflict once made available
    conflicts('~opengl ~opengles')

    # OpenGL ES requires OpenGL
    conflicts('~opengl +opengles')

    # https://gitlab.freedesktop.org/mesa/mesa/-/issues/5455
    conflicts('llvm@13.0.0:', when='@:21.3.1 +llvm')

    # requires native to be added to llvm_modules when using gallium swrast
    patch('https://cgit.freedesktop.org/mesa/mesa/patch/meson.build?id=054dd668a69acc70d47c73abe4646e96a1f23577', sha256='36096a178070e40217945e12d542dfe80016cb897284a01114d616656c577d73', when='@21.0.0:21.0.3')

    patch('mesa_check_llvm_version_suffix.patch', when='@21.2.3:')

    # 'auto' needed when shared llvm is built
    @when('^llvm~shared_libs')
    def patch(self):
        filter_file(
            r"_llvm_method = 'auto'",
            "_llvm_method = 'config-tool'",
            "meson.build")

    def meson_args(self):
        spec = self.spec
        args = [
            '-Dvulkan-drivers=',
            '-Dgallium-vdpau=disabled',
            '-Dgallium-xvmc=disabled',
            '-Dgallium-omx=disabled',
            '-Dgallium-va=disabled',
            '-Dgallium-xa=disabled',
            '-Dgallium-nine=false',
            '-Dgallium-opencl=disabled',
            '-Dbuild-tests=false',
            '-Dglvnd=false']
        args_platforms = []
        args_gallium_drivers = ['swrast']
        args_dri_drivers = []

        opt_enable = lambda c, o: '-D%s=%sabled' % (o, 'en' if c else 'dis')
        opt_bool = lambda c, o: '-D%s=%s' % (o, str(c).lower())
        if spec.target.family == 'arm' or spec.target.family == 'aarch64':
            args.append('-Dlibunwind=disabled')

        num_frontends = 0

        if spec.satisfies('@:20.3'):
            osmesa_enable, osmesa_disable = ('gallium', 'none')
        else:
            osmesa_enable, osmesa_disable = ('true', 'false')

        if '+osmesa' in spec:
            num_frontends += 1
            args.append('-Dosmesa={0}'.format(osmesa_enable))
        else:
            args.append('-Dosmesa={0}'.format(osmesa_disable))

        if '+glx' in spec:
            num_frontends += 1
            if '+egl' in spec:
                args.append('-Dglx=dri')
            else:
                args.append('-Dglx=gallium-xlib')
            args_platforms.append('x11')
        else:
            args.append('-Dglx=disabled')

        if '+egl' in spec:
            num_frontends += 1
            args.extend(['-Degl=enabled', '-Dgbm=enabled', '-Ddri3=enabled'])
            args_platforms.append('surfaceless')
        else:
            args.extend(
                ['-Degl=disabled', '-Dgbm=disabled', '-Ddri3=disabled'])

        args.append(opt_bool('+opengl' in spec, 'opengl'))
        args.append(opt_enable('+opengles' in spec, 'gles1'))
        args.append(opt_enable('+opengles' in spec, 'gles2'))

        args.append(opt_enable(num_frontends > 1, 'shared-glapi'))

        if '+llvm' in spec:
            # Fix builds on hosts where /usr/bin/llvm-config-* is found and provides an
            # incompatible version. Ensure that the llvm-config of spec['libllvm'] is
            # used.
            args.append('--native-file')
            args.append('meson-native-config.ini')
            mkdirp(self.build_directory)
            with working_dir(self.build_directory):
                with open('meson-native-config.ini', 'w') as native_config:
                    llvm_config = spec['libllvm'].prefix.bin + '/llvm-config'
                    native_config.write('[binaries]\n')
                    native_config.write("llvm-config = '{0}'\n".format(llvm_config))
            args.append('-Dllvm=enabled')
            args.append(opt_enable(
                '+llvm_dylib' in spec['libllvm'], 'shared-llvm'))
        else:
            args.append('-Dllvm=disabled')

        args_swr_arches = []
        if 'swr=auto' in spec:
            if 'avx' in spec.target:
                args_swr_arches.append('avx')
            if 'avx2' in spec.target:
                args_swr_arches.append('avx2')
            if 'avx512f' in spec.target:
                if 'avx512er' in spec.target:
                    args_swr_arches.append('knl')
                if 'avx512bw' in spec.target:
                    args_swr_arches.append('skx')
        else:
            if 'swr=avx' in spec:
                args_swr_arches.append('avx')
            if 'swr=avx2' in spec:
                args_swr_arches.append('avx2')
            if 'swr=knl' in spec:
                args_swr_arches.append('knl')
            if 'swr=skx' in spec:
                args_swr_arches.append('skx')

        if args_swr_arches:
            args_gallium_drivers.append('swr')
            args.append('-Dswr-arches=' + ','.join(args_swr_arches))

        # Add the remaining list args
        args.append('-Dplatforms=' + ','.join(args_platforms))
        args.append('-Dgallium-drivers=' + ','.join(args_gallium_drivers))
        args.append('-Ddri-drivers=' + ','.join(args_dri_drivers))

        return args

    @property
    def libs(self):
        spec = self.spec
        libs_to_seek = set()

        if '+osmesa' in spec:
            libs_to_seek.add('libOSMesa')

        if '+glx' in spec:
            libs_to_seek.add('libGL')

        if '+opengl' in spec:
            libs_to_seek.add('libGL')

        if '+opengles' in spec:
            libs_to_seek.add('libGLES')
            libs_to_seek.add('libGLES2')

        if libs_to_seek:
            return find_libraries(list(libs_to_seek),
                                  root=self.spec.prefix,
                                  recursive=True)
        return LibraryList()

    @property
    def osmesa_libs(self):
        return find_libraries('libOSMesa',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def glx_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)

    @property
    def gl_libs(self):
        return find_libraries('libGL',
                              root=self.spec.prefix,
                              recursive=True)
