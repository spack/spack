# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys


class Mesa(MesonPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"

    # Note that we always want to build from the git repo instead of a
    # tarball since the tarball has pre-generated files for certain versions
    # of LLVM while the git repo doesn't so it can adapt at build time to
    # whatever version of LLVM you're using.
    git      = "https://gitlab.freedesktop.org/mesa/mesa.git"

    version('19.0.0', tag='mesa-19.0.0')

    version('19.0.develop', branch='19.0')
    version('develop',      branch='master')

    depends_on('meson@0.45:', type='build')
    depends_on('binutils', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@3:', type='build')
    depends_on('py-mako@0.8.0:', type='build')
    depends_on('libxml2')
    depends_on('zlib')
    depends_on('expat')

    # Internal options
    variant('llvm', default=True, description="Enable LLVM.")
    variant('swr', values=any_combination_of('avx', 'avx2', 'knl', 'skx'),
            description="Enable the SWR driver.")
    # conflicts('~llvm', when='~swr=none')

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

    # Variant dependencies
    depends_on('llvm@6:', when='+llvm')
    depends_on('libx11',  when='+glx')
    depends_on('libxcb',  when='+glx')
    depends_on('libxext', when='+glx')

    def meson_args(self):
        spec = self.spec
        args = [
            '-Dglvnd=false',
            '-Dgallium-nine=false',
            '-Dgallium-omx=disabled',
            '-Dgallium-opencl=disabled',
            '-Dgallium-va=false',
            '-Dgallium-vdpau=false',
            '-Dgallium-xa=false',
            '-Dgallium-xvmc=false',
            '-Dvulkan-drivers=']
        args_platforms = []
        args_gallium_drivers = ['swrast']
        args_dri_drivers = []

        num_frontends = 0
        if '+osmesa' in spec:
            num_frontends += 1
            args.append('-Dosmesa=gallium')
        else:
            args.append('-Dosmesa=disabled')

        if '+glx' in spec:
            num_frontends += 1
            args.append('-Dglx=gallium-xlib')
            args_platforms.append('x11')
        else:
            args.append('-Dglx=disabled')

        if '+egl' in spec:
            num_frontends += 1
            args.extend(['-Degl=true', '-Dgbm=true'])
        else:
            args.extend(['-Degl=false', '-Dgbm=false'])

        if '+opengl' in spec:
            args.append('-Dopengl=true')
        else:
            args.append('-Dopengl=false')

        if '+opengles' in spec:
            args.extend(['-Dgles1=true', '-Dgles2=true'])
        else:
            args.extend(['-Dgles1=false', '-Dgles2=false'])

        if '+egl' in spec or '+osmesa' in spec:
            args_platforms.append('surfaceless')

        if num_frontends > 1:
            args.append('-Dshared-glapi=true')
        else:
            args.append('-Dshared-glapi=false')

        if '+llvm' in spec:
            args.append('-Dllvm=true')
            if '+link_dylib' in spec['llvm']:
                args.append('-Dshared-llvm=true')
            else:
                args.append('-Dshared-llvm=false')
        else:
            args.append('-Dllvm=false')

        args_swr_arches = []
        if 'swr=avx' in spec:
            args_swr_arches.append('avx')
        if 'swr=avx2' in spec:
            args_swr_arches.append('avx2')
        if 'swr=knl' in spec:
            args_swr_arches.append('knl')
        if 'swr=skx' in spec:
            args_swr_arches.append('skx')
        if args_swr_arches:
            if '+llvm' not in spec:
                raise SpecError('Variant swr requires +llvm')
            args_gallium_drivers.append('swr')
            args.append('-Dswr-arches=' + ','.join(args_swr_arches))

        # Add the remaining list args
        args.append('-Dplatforms=' + ','.join(args_platforms))
        args.append('-Dgallium-drivers=' + ','.join(args_gallium_drivers))
        args.append('-Ddri-drivers=' + ','.join(args_dri_drivers))

        return args
