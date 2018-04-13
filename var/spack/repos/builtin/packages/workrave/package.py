##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
from spack import *
from shutil import copyfile


class Workrave(AutotoolsPackage):
    """Workrave is a program that assists in the recovery and prevention of
       Repetitive Strain Injury (RSI). The program frequently alerts you to
       take micro-pauses, rest breaks and restricts you to your daily limit.
       The program runs on GNU/Linux and Microsoft Windows.
    """

    homepage = "http://www.workrave.org/"
    url      = "https://github.com/rcaelers/workrave/archive/v1_10_20.tar.gz"

    version('1_10_20', '095567c10311bd2c1a52f98035cc8590')
    version('1_10_19', 'a87ed53d5b321133e8b6b98fd715507b')
    version('1_10_18', 'd36c2aba0485116b831d5b36a862f343')
    version('1_10_17', 'ba829bb2c0ec999b3194b4d845549c39')
    version('1_10_16', 'b9bf77bfe0c909fff56759e7dda40f9d')
    version('1_10_15', '4a70c2e325503249d1a40fcc236d6802')
    version('1_10_14', '67108d993719d9438a1b69f0cb8fc9b8')
    version('1_10_13', 'd5e7110dfb0b0a31c909405913ac2a75')
    version('1_10_12', '0bfbaa1dc35901ffa8f1a3676421a992')
    version('1_10_10', 'cf827672c8a1ece074f8ddfcf73d0fe2')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('libx11')
    depends_on('py-cheetah')
    depends_on('glib')
    depends_on('glibmm')
    depends_on('gtkplus')
    depends_on('gtkmm@2.17.1')
    depends_on('libsigcpp')

    # adds #include <time.h> to a workrave test
    patch('add_time_header.patch')

    # removes call to missing glimm api function
    patch('signal_size_changed.patch', when='@1.10.0')

    # removes call to missing gtkmm api function
    patch('dont_get_widget.patch')

    # removes gettext which canot be use with intltool
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=724555
    # https://bugzilla.gnome.org/show_bug.cgi?id=708673#c4
    patch('no_gettext.patch')

    @run_before('autoreconf')
    def extra_m4(self):
        # add a couple m4 macros used during autoreconf
        # https://github.com/rcaelers/workrave/issues/95
        m4files = ['ax_cxx_compile_stdcxx_11.m4', 'ax_cxx_compile_stdcxx.m4']
        for fname in m4files:
            src = '%s/%s' % (self.package_dir, fname)
            dest = '%s/m4/%s' % (self.stage.source_path, fname)
            copyfile(src, dest)

    def configure_args(self):
        specs = self.spec.traverse(root=False)
        pkgconfdirs = ['%s/pkgconfig' % s.prefix.lib
                       for s in specs if not s.external]
        return ['PKG_CONFIG_PATH=%s' % ':'.join(pkgconfdirs)]
