##############################################################################
# Copyright (c) 2017 Milton Woods, Mark Olesen
#
# This file is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
#
# Notes
# - swr: need better handling of C++14 constructs
#        may need to export LD_LIBRARY_PATH for dependent packages
#
##############################################################################

from spack import *


class Mesa(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL specification
     - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "https://mesa.freedesktop.org/archive/13.0.6/mesa-13.0.6.tar.xz"
    list_url = "https://mesa.freedesktop.org/archive"
    list_depth = 2

    version('17.1.5', '6cf936fbcaadd98924298a7009e8265d')
    version('17.1.4', 'be2ef7c9edec23b07f74f6512a6a6fa5')
    version('17.1.3', '1946a93d543bc219427e2bebe2ac4752')
    version('17.1.1', 'a4844bc6052578574f9629458bcbb749')
    version('13.0.6', '1e5a769bc6cfd839cf3febcb179c27cc')
    version('12.0.6', '1a3d4fea0656c208db59289e4ed33b3f')
    version('12.0.3', '1113699c714042d8c4df4766be8c57d8')

    variant('swrender', default=True,
            description="Build with (gallium) software rendering.")
    variant('hwrender', default=False,
            description="Build with (DRI) hardware rendering.")
    variant('llvm', default=False,
            description="Use llvm for rendering pipes.")

    # General dependencies
    depends_on('pkg-config@0.9.0:', type='build')
    depends_on('flex@2.5.35:', type='build')
    depends_on('bison@2.4.1:', type='build')
    depends_on('binutils', type='build')
    depends_on('python@2.6.4:', type='build')
    depends_on('py-mako@0.3.4:', type='build')
    depends_on('gettext')
    depends_on('icu4c')
    depends_on('expat')
    depends_on('libpthread-stubs')
    depends_on('openssl')
    depends_on('xproto')
    depends_on('glproto@1.4.14:')
    depends_on('presentproto@1.0:')
    depends_on('libxcb@1.9.3:')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxshmfence@1.1:')
    depends_on('libxdamage')
    depends_on('libxfixes')
    depends_on('libxv')
    depends_on('libxvmc')

    # For DRI and hardware acceleration
    depends_on('dri2proto@2.6:', type='build')
    depends_on('dri3proto@1.0:', type='build')
    depends_on('libdrm')

    depends_on('llvm@:3.8.1+link_dylib', when='@12:12.99+llvm')
    depends_on('llvm@:3.9.1+link_dylib', when='@13:13.99+llvm')
    depends_on('llvm+link_dylib', when='+llvm')
    depends_on('libelf', when='+llvm')

    def configure_args(self):
        """Build drivers for platforms supported by spack;
        exclude drivers for embedded systems.
        """
        spec = self.spec
        args = ['--enable-glx', '--enable-glx-tls']
        drivers = []

        if '+swrender' in spec:
            drivers = ['swrast']
            args.extend([
                '--disable-osmesa',
                '--enable-gallium-osmesa',
                '--enable-texture-float',
            ])
            if '+llvm' in spec:
                # For @17.1.1:17.1.2 the swr driver requires C++14 support
                # Should be fixed in 17.1.3, but can still encounter problems
                if spec.version >= Version('17'):
                    if spec.satisfies('%gcc@4.9:'):
                        drivers.append('swr')
                else:
                    drivers.append('swr')
        else:
            args.append('--disable-gallium-osmesa')
            # Fallback for "~hwrender~swrender" -> old osmesa
            if '~hwrender' in spec:
                args.append('--enable-osmesa')

        if '+hwrender' in spec:
            args.extend([
                '--enable-xa',
                '--with-egl-platforms=x11,drm'
            ])
            drivers.extend([
                'svga', 'i915', 'r600', 'nouveau', 'virgl'
            ])

            # These hardware drivers need llvm
            if '+llvm' in spec:
                drivers.extend(['r300', 'radeonsi'])

        else:
            args.extend([
                '--disable-xa',
                '--disable-dri',
                '--disable-dri3',
                '--disable-egl',
                '--disable-gbm',
                '--disable-xvmc',
            ])

        if '+llvm' in spec:
            if self.spec.version < Version('17'):
                args.append('--enable-gallium-llvm')
            else:
                args.append('--enable-llvm')
            if '+link_dylib' in self.spec['llvm']:
                args.append('--enable-llvm-shared-libs')
            else:
                args.append('--disable-llvm-shared-libs')
            args.append('--with-llvm-prefix=%s' % spec['llvm'].prefix)

        args.append('--with-gallium-drivers=' + ','.join(drivers))

        # Avoid errors due to missing clock_gettime symbol:
        arch = spec.architecture
        if arch.platform == 'linux':
            args.append('LIBS=-lrt')

        return args

    def configure(self, spec, prefix):
        """Configure mesa, detecting if libsysfs is required
        for DRI support on the build host.
        """
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()

	try:
	    # First attempt uses libudev:
	    configure(*options)
	except ProcessError:
	    if '+hwrender' in spec and not spec.satisfies('@13:'):
		print('Configuring with libudev failed ... '
		      ' trying libsysfs ...')
		options.append('--enable-sysfs')
		configure(*options)
	    else:
		raise
