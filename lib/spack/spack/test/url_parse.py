##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
"""\
This file has a bunch of versions tests taken from the excellent version
detection in Homebrew.
"""
import unittest

import spack.url as url


class UrlParseTest(unittest.TestCase):

    def assert_not_detected(self, string):
        self.assertRaises(
            url.UndetectableVersionError, url.parse_name_and_version, string)

    def check(self, name, v, string, **kwargs):
        # Make sure correct name and version are extracted.
        parsed_name, parsed_v = url.parse_name_and_version(string)
        self.assertEqual(parsed_name, name)
        self.assertEqual(parsed_v, url.Version(v))

        # Some URLs (like boost) are special and need to override the
        # built-in functionality.
        if kwargs.get('no_check_url', False):
            return

        # Make sure Spack formulates the right URL when we try to
        # build one with a specific version.
        self.assertEqual(string, url.substitute_version(string, v))

    def test_wwwoffle_version(self):
        self.check(
            'wwwoffle', '2.9h',
            'http://www.gedanken.demon.co.uk/download-wwwoffle/wwwoffle-2.9h.tgz')

    def test_version_sourceforge_download(self):
        self.check(
            'foo-bar', '1.21',
            'http://sourceforge.net/foo_bar-1.21.tar.gz/download')
        self.check(
            'foo-bar', '1.21',
            'http://sf.net/foo_bar-1.21.tar.gz/download')

    def test_no_version(self):
        self.assert_not_detected('http://example.com/blah.tar')
        self.assert_not_detected('foo')

    def test_version_all_dots(self):
        self.check(
            'foo-bar-la', '1.14', 'http://example.com/foo.bar.la.1.14.zip')

    def test_version_underscore_separator(self):
        self.check(
            'grc', '1.1',
            'http://example.com/grc_1.1.tar.gz')

    def test_boost_version_style(self):
        self.check(
            'boost', '1.39.0',
            'http://example.com/boost_1_39_0.tar.bz2',
            no_check_url=True)

    def test_erlang_version_style(self):
        self.check(
            'otp', 'R13B',
            'http://erlang.org/download/otp_src_R13B.tar.gz')

    def test_another_erlang_version_style(self):
        self.check(
            'otp', 'R15B01',
            'https://github.com/erlang/otp/tarball/OTP_R15B01')

    def test_yet_another_erlang_version_style(self):
        self.check(
            'otp', 'R15B03-1',
            'https://github.com/erlang/otp/tarball/OTP_R15B03-1')

    def test_p7zip_version_style(self):
        self.check(
            'p7zip', '9.04',
            'http://kent.dl.sourceforge.net/sourceforge/p7zip/p7zip_9.04_src_all.tar.bz2')

    def test_new_github_style(self):
        self.check(
            'libnet', '1.1.4',
            'https://github.com/sam-github/libnet/tarball/libnet-1.1.4')

    def test_gloox_beta_style(self):
        self.check(
            'gloox', '1.0-beta7',
            'http://camaya.net/download/gloox-1.0-beta7.tar.bz2')

    def test_sphinx_beta_style(self):
        self.check(
            'sphinx', '1.10-beta',
            'http://sphinxsearch.com/downloads/sphinx-1.10-beta.tar.gz')

    def test_astyle_verson_style(self):
        self.check(
            'astyle', '1.23',
            'http://kent.dl.sourceforge.net/sourceforge/astyle/astyle_1.23_macosx.tar.gz')

    def test_version_dos2unix(self):
        self.check(
            'dos2unix', '3.1',
            'http://www.sfr-fresh.com/linux/misc/dos2unix-3.1.tar.gz')

    def test_version_internal_dash(self):
        self.check(
            'foo-arse', '1.1-2',
            'http://example.com/foo-arse-1.1-2.tar.gz')

    def test_version_single_digit(self):
        self.check(
            'foo-bar', '45',
            'http://example.com/foo_bar.45.tar.gz')

    def test_noseparator_single_digit(self):
        self.check(
            'foo-bar', '45',
            'http://example.com/foo_bar45.tar.gz')

    def test_version_developer_that_hates_us_format(self):
        self.check(
            'foo-bar-la', '1.2.3',
            'http://example.com/foo-bar-la.1.2.3.tar.gz')

    def test_version_regular(self):
        self.check(
            'foo-bar', '1.21',
            'http://example.com/foo_bar-1.21.tar.gz')

    def test_version_gitlab(self):
        self.check(
             'vtk', '7.0.0',
             'https://gitlab.kitware.com/vtk/vtk/repository/'
             'archive.tar.bz2?ref=v7.0.0')
        self.check(
             'icet', '1.2.3',
             'https://gitlab.kitware.com/icet/icet/repository/'
             'archive.tar.gz?ref=IceT-1.2.3')
        self.check(
             'foo', '42.1337',
             'http://example.com/org/foo/repository/'
             'archive.zip?ref=42.1337bar')

    def test_version_github(self):
        self.check(
            'yajl', '1.0.5',
            'http://github.com/lloyd/yajl/tarball/1.0.5')

    def test_version_github_with_high_patch_number(self):
        self.check(
            'yajl', '1.2.34',
            'http://github.com/lloyd/yajl/tarball/v1.2.34')

    def test_yet_another_version(self):
        self.check(
            'mad', '0.15.1b',
            'http://example.com/mad-0.15.1b.tar.gz')

    def test_lame_version_style(self):
        self.check(
            'lame', '398-2',
            'http://kent.dl.sourceforge.net/sourceforge/lame/lame-398-2.tar.gz')

    def test_ruby_version_style(self):
        self.check(
            'ruby', '1.9.1-p243',
            'ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.1-p243.tar.gz')

    def test_omega_version_style(self):
        self.check(
            'omega', '0.80.2',
            'http://www.alcyone.com/binaries/omega/omega-0.80.2-src.tar.gz')

    def test_rc_style(self):
        self.check(
            'libvorbis', '1.2.2rc1',
            'http://downloads.xiph.org/releases/vorbis/libvorbis-1.2.2rc1.tar.bz2')

    def test_dash_rc_style(self):
        self.check(
            'js', '1.8.0-rc1',
            'http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz')

    def test_angband_version_style(self):
        self.check(
            'angband', '3.0.9b',
            'http://rephial.org/downloads/3.0/angband-3.0.9b-src.tar.gz')

    def test_stable_suffix(self):
        self.check(
            'libevent', '1.4.14b',
            'http://www.monkey.org/~provos/libevent-1.4.14b-stable.tar.gz')

    def test_debian_style_1(self):
        self.check(
            'sl', '3.03',
            'http://ftp.de.debian.org/debian/pool/main/s/sl/sl_3.03.orig.tar.gz')

    def test_debian_style_2(self):
        self.check(
            'mmv', '1.01b',
            'http://ftp.de.debian.org/debian/pool/main/m/mmv/mmv_1.01b.orig.tar.gz')

    def test_imagemagick_style(self):
        self.check(
            'imagemagick', '6.7.5-7',

            'http://downloads.sf.net/project/machomebrew/mirror/ImageMagick-6.7.5-7.tar.bz2')

    def test_dash_version_dash_style(self):
        self.check(
            'antlr', '3.4',
            'http://www.antlr.org/download/antlr-3.4-complete.jar')

    def test_apache_version_style(self):
        self.check(
            'apache-cassandra', '1.2.0-rc2',
            'http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin.tar.gz')

    def test_jpeg_style(self):
        self.check(
            'jpegsrc', '8d',
            'http://www.ijg.org/files/jpegsrc.v8d.tar.gz')

    def test_pypy_version(self):
        self.check(
            'pypy', '1.4.1',
            'http://pypy.org/download/pypy-1.4.1-osx.tar.bz2')

    def test_openssl_version(self):
        self.check(
            'openssl', '0.9.8s',
            'http://www.openssl.org/source/openssl-0.9.8s.tar.gz')

    def test_xaw3d_version(self):
        self.check(
            'xaw3d', '1.5E',
            'ftp://ftp.visi.com/users/hawkeyd/X/Xaw3d-1.5E.tar.gz')

    def test_fann_version(self):
        self.check(
            'fann', '2.1.0beta',
            'http://downloads.sourceforge.net/project/fann/fann/2.1.0beta/fann-2.1.0beta.zip')

    def test_iges_version(self):
        self.check(
            'grads', '2.0.1',
            'ftp://iges.org/grads/2.0/grads-2.0.1-bin-darwin9.8-intel.tar.gz')

    def test_haxe_version(self):
        self.check(
            'haxe', '2.08',
            'http://haxe.org/file/haxe-2.08-osx.tar.gz')

    def test_imap_version(self):
        self.check(
            'imap', '2007f',
            'ftp://ftp.cac.washington.edu/imap/imap-2007f.tar.gz')

    def test_suite3270_version(self):
        self.check(
            'suite3270', '3.3.12ga7',
            'http://sourceforge.net/projects/x3270/files/x3270/3.3.12ga7/suite3270-3.3.12ga7-src.tgz')

    def test_synergy_version(self):
        self.check(
            'synergy', '1.3.6p2',
            'http://synergy.googlecode.com/files/synergy-1.3.6p2-MacOSX-Universal.zip')

    def test_mvapich2_19_version(self):
        self.check(
            'mvapich2', '1.9',
            'http://mvapich.cse.ohio-state.edu/download/mvapich2/mv2/mvapich2-1.9.tgz')

    def test_mvapich2_20_version(self):
        self.check(
            'mvapich2', '2.0',
            'http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.0.tar.gz')

    def test_hdf5_version(self):
        self.check(
            'hdf5', '1.8.13',
            'http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-1.8.13.tar.bz2')

    def test_scalasca_version(self):
        self.check(
            'cube', '4.2.3',
            'http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz')
        self.check(
            'cube', '4.3-TP1',
            'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz')

    def test_mpileaks_version(self):
        self.check(
            'mpileaks', '1.0',
            'https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz')
        self.check(
            'mpileaks', '1.0',
            'https://github.com/hpc/mpileaks/releases/download/1.0/mpileaks-1.0.tar.gz')

    def test_gcc_version(self):
        self.check(
            'gcc', '4.4.7',
            'http://open-source-box.org/gcc/gcc-4.4.7/gcc-4.4.7.tar.bz2')

    def test_gcc_version_precedence(self):
        # prefer the version in the tarball, not in the url prefix.
        self.check(
            'gcc', '4.4.7',
            'http://open-source-box.org/gcc/gcc-4.9.2/gcc-4.4.7.tar.bz2')

    def test_github_raw_url(self):
        self.check(
            'powerparser', '2.0.7',
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true')

    def test_r_xml_version(self):
        self.check(
            'xml', '3.98-1.4',
            'https://cran.r-project.org/src/contrib/XML_3.98-1.4.tar.gz')

    def test_nco_version(self):
        self.check(
            'nco', '4.6.2-beta03',
            'https://github.com/nco/nco/archive/4.6.2-beta03.tar.gz')

        self.check(
            'nco', '4.6.3-alpha04',
            'https://github.com/nco/nco/archive/4.6.3-alpha04.tar.gz')

    def test_yorick_version(self):
        self.check(
            'yorick', '2_2_04',
            'https://github.com/dhmunro/yorick/archive/y_2_2_04.tar.gz')

    def test_luaposix_version(self):
        self.check(
            'luaposix', '33.4.0',
            'https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz')

    def test_sionlib_version(self):
        self.check(
            'sionlib', '1.7.1',
            'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1')
