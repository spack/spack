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
import os
import unittest

from spack.url import *


class UrlStripVersionSuffixesTest(unittest.TestCase):

    def check(self, before, after):
        stripped = strip_version_suffixes(before)
        self.assertEqual(stripped, after)

    def test_no_suffix(self):
        self.check('rgb-1.0.6',
                   'rgb-1.0.6')

    def test_misleading_prefix(self):
        self.check('jpegsrc.v9b',
                   'jpegsrc.v9b')
        self.check('turbolinux702',
                   'turbolinux702')
        self.check('converge_install_2.3.16',
                   'converge_install_2.3.16')

    # Download type

    def test_src(self):
        self.check('apache-ant-1.9.7-src',
                   'apache-ant-1.9.7')
        self.check('go1.7.4.src',
                   'go1.7.4')

    def test_source(self):
        self.check('bowtie2-2.2.5-source',
                   'bowtie2-2.2.5')
        self.check('grib_api-1.17.0-Source',
                   'grib_api-1.17.0')

    def test_full(self):
        self.check('julia-0.4.3-full',
                   'julia-0.4.3')

    def test_bin(self):
        self.check('apache-maven-3.3.9-bin',
                   'apache-maven-3.3.9')

    # Download version

    def test_stable(self):
        self.check('libevent-2.0.21-stable',
                   'libevent-2.0.21')

    def test_final(self):
        self.check('2.6.7-final',
                   '2.6.7')

    def test_rel(self):
        self.check('v1.9.5.1rel',
                   'v1.9.5.1')

    def test_orig(self):
        self.check('dash_0.5.5.1.orig',
                   'dash_0.5.5.1')

    # License

    def test_gpl(self):
        self.check('cppad-20170114.gpl',
                   'cppad-20170114')

    # OS

    def test_linux(self):
        self.check('astyle_2.04_linux',
                   'astyle_2.04')

    def test_unix(self):
        self.check('install-tl-unx',
                   'install-tl')

    def test_macos(self):
        self.check('astyle_1.23_macosx',
                   'astyle_1.23')
        self.check('haxe-2.08-osx',
                   'haxe-2.08')

    # PyPI

    def test_wheel(self):
        self.check('entrypoints-0.2.2-py2.py3-none-any.whl',
                   'entrypoints-0.2.2')

    # Combinations of multiple patterns

    def test_complex_all(self):
        self.check('p7zip_9.04_src_all',
                   'p7zip_9.04')

    def test_complex_run(self):
        self.check('cuda_8.0.44_linux.run',
                   'cuda_8.0.44')

    def test_complex_file(self):
        self.check('ack-2.14-single-file',
                   'ack-2.14')

    def test_complex_arch(self):
        self.check('VizGlow_v2.2alpha17-R21November2016-Linux-x86_64-Install',
                   'VizGlow_v2.2alpha17-R21November2016')
        self.check('jdk-8u92-linux-x64',
                   'jdk-8u92')
        self.check('cuda_6.5.14_linux_64.run',
                   'cuda_6.5.14')

    def test_complex_with(self):
        self.check('mafft-7.221-with-extensions-src',
                   'mafft-7.221')
        self.check('spark-2.0.0-bin-without-hadoop',
                   'spark-2.0.0')

    def test_complex_public(self):
        self.check('dakota-6.3-public.src',
                   'dakota-6.3')

    def test_complex_universal(self):
        self.check('synergy-1.3.6p2-MacOSX-Universal',
                   'synergy-1.3.6p2')

class UrlParseOffsetTest(unittest.TestCase):

    def check(self, name, noffset, ver, voffset, path):
        # Make sure parse_name_offset and parse_name_version are working
        v, vstart, vlen, vi, vre = parse_version_offset(path)
        n, nstart, nlen, ni, nre = parse_name_offset(path, v)

        self.assertEqual(n, name)
        self.assertEqual(v, ver)
        self.assertEqual(nstart, noffset)
        self.assertEqual(vstart, voffset)

    def test_name_in_path(self):
        self.check(
            'antlr', 25, '2.7.7', 40,
            'https://github.com/antlr/antlr/tarball/v2.7.7')

    def test_name_in_stem(self):
        self.check(
            'gmp', 32, '6.0.0a', 36,
            'https://gmplib.org/download/gmp/gmp-6.0.0a.tar.bz2')

    def test_name_in_suffix(self):
        # Don't think I've ever seen one of these before
        # We don't look for it, so it would probably fail anyway
        pass

    def test_version_in_path(self):
        self.check(
            'nextflow', 31, '0.20.1', 59,
            'https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow')

    def test_version_in_stem(self):
        self.check(
            'zlib', 24, '1.2.10', 29,
            'http://zlib.net/fossils/zlib-1.2.10.tar.gz')
        self.check(
            'slepc', 51, '3.6.2', 57,
            'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz')
        self.check(
            'cloog', 61, '0.18.1', 67,
            'http://www.bastoul.net/cloog/pages/download/count.php3?url=./cloog-0.18.1.tar.gz')
        self.check(
            'libxc', 58, '2.2.2', 64,
            'http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz')

    def test_version_in_suffix(self):
        self.check(
            'swiftsim', 36, '0.3.0', 76,
            'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0')
        self.check(
            'sionlib', 30, '1.7.1', 59,
            'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1')


class UrlParseNameAndVersionTest(unittest.TestCase):

    def assert_not_detected(self, string):
        self.assertRaises(
            UndetectableVersionError, parse_name_and_version, string)

    def check(self, name, v, string, **kwargs):
        # Make sure correct name and version are extracted.
        parsed_name, parsed_v = parse_name_and_version(string)
        self.assertEqual(parsed_name, name)
        self.assertEqual(parsed_v, Version(v))

        # Some URLs (like boost) are special and need to override the
        # built-in functionality.
        if kwargs.get('no_check_url', False):
            return

        # Make sure Spack formulates the right URL when we try to
        # build one with a specific version.
        self.assertEqual(string, substitute_version(string, v))

    # Common Repositories

    def test_github_downloads(self):
        # name/archive/ver.ver
        self.check(
            'nco', '4.6.2',
            'https://github.com/nco/nco/archive/4.6.2.tar.gz')
        # name/archive/vver.ver
        self.check(
            'vim', '8.0.0134',
            'https://github.com/vim/vim/archive/v8.0.0134.tar.gz')
        # name/archive/name-ver.ver
        self.check(
            'oce', '0.18',
            'https://github.com/tpaviot/oce/archive/OCE-0.18.tar.gz')
        # name/releases/download/vver/name-ver.ver
        self.check(
            'libmesh', '1.0.0',
            'https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2')
        # name/tarball/vver.ver
        self.check(
            'git', '2.7.1',
            'https://github.com/git/git/tarball/v2.7.1')
        # name/zipball/vver.ver
        self.check(
            'git', '2.7.1',
            'https://github.com/git/git/zipball/v2.7.1')

    def test_gitlab_downloads(self):
        # name/repository/archive.ext?ref=vver.ver
        self.check(
            'swiftsim', '0.3.0',
            'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0')
        # name/repository/archive.ext?ref=name-ver.ver
        self.check(
             'icet', '1.2.3',
             'https://gitlab.kitware.com/icet/icet/repository/archive.tar.gz?ref=IceT-1.2.3')

    def test_bitbucket_downloads(self):
        # name/get/ver.ver
        self.check(
            'eigen', '3.2.7',
            'https://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2')
        # name/get/vver.ver
        self.check(
            'hoomd-blue', '1.3.3',
            'https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2')
        # name/downloads/name-ver.ver
        self.check(
            'dolfin', '2016.1.0',
            'https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-2016.1.0.tar.gz')

    def test_sourceforge_downloads(self):
        # name-ver.ver
        self.check(
            'libpng', '1.6.27',
            'http://download.sourceforge.net/libpng/libpng-1.6.27.tar.gz')
        self.check(
            'lcms2', '2.6',
            'http://downloads.sourceforge.net/project/lcms/lcms/2.6/lcms2-2.6.tar.gz')
        self.check(
            'modules', '3.2.10',
            'http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz')
        # name-ver.ver.ext/download
        self.check(
            'glew', '2.0.0',
            'https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download')

    def test_cran_downloads(self):
        # name.name_ver.ver-ver.ver
        self.check(
            'th-data', '1.0-8',
            'https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz')
        self.check(
            'knitr', '1.14',
            'https://cran.rstudio.com/src/contrib/knitr_1.14.tar.gz')
        self.check(
            'devtools', '1.12.0',
            'https://cloud.r-project.org/src/contrib/devtools_1.12.0.tar.gz')

    def test_pypi_downloads(self):
        # name.name_name-ver.ver
        self.check(
            '3to2', '1.1.1',
            'https://pypi.python.org/packages/source/3/3to2/3to2-1.1.1.zip')
        self.check(
            'mpmath', '0.19',
            'https://pypi.python.org/packages/source/m/mpmath/mpmath-all-0.19.tar.gz')
        self.check(
            'pandas', '0.16.0',
            'https://pypi.python.org/packages/source/p/pandas/pandas-0.16.0.tar.gz#md5=bfe311f05dc0c351f8955fbd1e296e73')
        self.check(
            'sphinx-rtd-theme', '0.1.10a0',
            'https://pypi.python.org/packages/da/6b/1b75f13d8aa3333f19c6cdf1f0bc9f52ea739cae464fbee050307c121857/sphinx_rtd_theme-0.1.10a0.tar.gz')
        self.check(
            'backports-ssl-match-hostname', '3.5.0.1',
            'https://pypi.io/packages/source/b/backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz')

    def test_bazaar_downloads(self):
        self.check(
            'libvterm', '681',
            'http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr681.tar.gz')

    # Common Tarball Formats

    def test_no_separators(self):
        # namever
        self.check(
            'turbo', '702',
            'file://{0}/turbolinux702.tar.gz'.format(os.getcwd()))
        self.check(
            'nauty', '26r7',
            'http://pallini.di.uniroma1.it/nauty26r7.tar.gz')

    def test_version_only(self):
        # ver.ver
        self.check(
            'eigen', '3.2.7',
            'https://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2')
        # ver.ver-ver
        self.check(
            'imagemagick', '7.0.2-7',
            'https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz')
        # vver.ver
        self.check(
            'cgns', '3.3.0',
            'https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz')
        # vver_ver
        self.check(
            'luafilesystem', '1_6_3',
            'https://github.com/keplerproject/luafilesystem/archive/v1_6_3.tar.gz')

    def test_dashes_only(self):
        # name-name-ver-ver
        self.check(
            'panda', '2016-03-07',
            'http://comopt.ifi.uni-heidelberg.de/software/PANDA/downloads/panda-2016-03-07.tar')
        self.check(
            'gts-snapshot', '121130',
            'http://gts.sourceforge.net/tarballs/gts-snapshot-121130.tar.gz')

    def test_underscores_only(self):
        # name_name_ver_ver
        self.check(
            'tinyxml', '2_6_2',
            'https://sourceforge.net/projects/tinyxml/files/tinyxml/2.6.2/tinyxml_2_6_2.tar.gz')
        self.check(
            'boost', '1_55_0',
            'http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2')

    def test_dots_only(self):
        # name.name.ver.ver
        self.check(
            'prank', '150803',
            'http://wasabiapp.org/download/prank/prank.source.150803.tgz')
        self.check(
            'jpeg', '9b',
            'http://www.ijg.org/files/jpegsrc.v9b.tar.gz')
        # name.namever.ver
        self.check(
            'atlas', '3.11.34',
            'http://sourceforge.net/projects/math-atlas/files/Developer%20%28unstable%29/3.11.34/atlas3.11.34.tar.bz2')
        self.check(
            'visit', '2.10.1',
            'http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz')
        self.check(
            'geant', '4.10.01.p03',
            'http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz')

    def test_dash_dot(self):
        # name-name-ver.ver
        # digit in name
        self.check(
            'm4', '1.4.17',
            'https://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz')
        # letter in version
        self.check(
            'gmp', '6.0.0a',
            'https://gmplib.org/download/gmp/gmp-6.0.0a.tar.bz2')
        # version starts with 'v'
        self.check(
            'launchmon', '1.0.2',
            'https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz')

    def test_dash_underscore(self):
        # name-name-ver_ver
        self.check(
            'icu4c', '57_1',
            'http://download.icu-project.org/files/icu4c/57.1/icu4c-57_1-src.tgz')

    def test_underscore_dot(self):
        # name_name_ver.ver
        self.check(
            'superlu-dist', '4.1',
            'http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.1.tar.gz')
        self.check(
            'pexsi', '0.9.0',
            'https://math.berkeley.edu/~linlin/pexsi/download/pexsi_v0.9.0.tar.gz')
        # name_name.ver.ver
        self.check(
            'fer', '696',
            'ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v696.tar.gz')

    def test_dash_dot_dash_dot(self):
        # name-name-ver.ver-ver.ver
        self.check(
            'sowing', '1.1.23-p1',
            'http://ftp.mcs.anl.gov/pub/petsc/externalpackages/sowing-1.1.23-p1.tar.gz')
        self.check(
            'bib2xhtml', '3.0-15-gf506',
            'http://www.spinellis.gr/sw/textproc/bib2xhtml/bib2xhtml-v3.0-15-gf506.tar.gz')
        # namever.ver-ver.ver
        self.check(
            'go', '1.4-bootstrap-20161024',
            'https://storage.googleapis.com/golang/go1.4-bootstrap-20161024.tar.gz')

    def test_underscore_dash_dot(self):
        # name_name-ver.ver
        self.check(
            'the-silver-searcher', '0.32.0',
            'http://geoff.greer.fm/ag/releases/the_silver_searcher-0.32.0.tar.gz')
        self.check(
            'sphinx-rtd-theme', '0.1.10a0',
            'https://pypi.python.org/packages/source/s/sphinx_rtd_theme/sphinx_rtd_theme-0.1.10a0.tar.gz')

    def test_dot_underscore_dot_dash_dot(self):
        # name.name_ver.ver-ver.ver
        self.check(
            'th-data', '1.0-8',
            'https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz')
        self.check(
            'xml', '3.98-1.4',
            'https://cran.r-project.org/src/contrib/XML_3.98-1.4.tar.gz')

    def test_dash_dot_underscore_dot(self):
        # name-name-ver.ver_ver.ver
        self.check(
            'pypar', '2.1.5_108',
            'https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-2.1.5_108.tgz')

    # Weird URLS

    def test_version_in_path(self):
        # github.com/repo/name/releases/download/name-vver/name
        self.check(
            'nextflow', '0.20.1',
            'https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow')

    def test_suffix_queries(self):
        self.check(
            'swiftsim', '0.3.0',
            'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0')
        self.check(
            'sionlib', '1.7.1',
            'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1')

    def test_stem_queries(self):
        self.check(
            'slepc', '3.6.2',
            'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz')
        self.check(
            'otf', '1.12.5salmon',
            'http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz')

    def test_single_character_name(self):
        self.check(
            'r', '3.3.2',
            'https://cloud.r-project.org/src/base/R-3/R-3.3.2.tar.gz')

    def test_single_digit_version(self):
        pass

    def plus_in_name(self):
        # FIXME: We should probably auto-convert these to 'plus'
        self.check(
            'gtk+', '2.24.31',
            'http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.31.tar.xz')
        self.check(
            'voro++', '0.4.6',
            'http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz')

    def test_no_version(self):
        self.assert_not_detected('http://www.netlib.org/blas/blast-forum/cblas.tgz')
        self.assert_not_detected('http://www.netlib.org/voronoi/triangle.zip')

    def test_download_php(self):
        # Name comes before download.php
        self.check(
            'sionlib', 30, '1.7.1', 59,
            'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1')
        # Ignore download.php
        self.check(
            'slepc', 51, '3.6.2', 57,
            'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz')
        self.check(
            'scientificpython', '2.8.1',
            'https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz')

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

    def test_gloox_beta_style(self):
        self.check(
            'gloox', '1.0-beta7',
            'http://camaya.net/download/gloox-1.0-beta7.tar.bz2')

    def test_sphinx_beta_style(self):
        self.check(
            'sphinx', '1.10-beta',
            'http://sphinxsearch.com/downloads/sphinx-1.10-beta.tar.gz')

    def test_ruby_version_style(self):
        self.check(
            'ruby', '1.9.1-p243',
            'ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.1-p243.tar.gz')

    def test_rc_style(self):
        self.check(
            'libvorbis', '1.2.2rc1',
            'http://downloads.xiph.org/releases/vorbis/libvorbis-1.2.2rc1.tar.bz2')

    def test_dash_rc_style(self):
        self.check(
            'js', '1.8.0-rc1',
            'http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz')

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

    def test_imap_version(self):
        self.check(
            'imap', '2007f',
            'ftp://ftp.cac.washington.edu/imap/imap-2007f.tar.gz')

    def test_suite3270_version(self):
        self.check(
            'suite3270', '3.3.12ga7',
            'http://sourceforge.net/projects/x3270/files/x3270/3.3.12ga7/suite3270-3.3.12ga7-src.tgz')

    def test_scalasca_version(self):
        self.check(
            'cube', '4.2.3',
            'http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz')
        self.check(
            'cube', '4.3-TP1',
            'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz')

    def test_github_raw_url(self):
        self.check(
            'powerparser', '2.0.7',
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true')

    def test_nco_version(self):
        self.check(
            'nco', '4.6.2-beta03',
            'https://github.com/nco/nco/archive/4.6.2-beta03.tar.gz')

        self.check(
            'nco', '4.6.3-alpha04',
            'https://github.com/nco/nco/archive/4.6.3-alpha04.tar.gz')

    def test_luaposix_version(self):
        self.check(
            'luaposix', '33.4.0',
            'https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz')
