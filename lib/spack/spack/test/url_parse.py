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
"""Tests Spack's ability to parse the name and version of a package
based on its URL.
"""

import os
import pytest

from spack.url import parse_name_offset, parse_version_offset
from spack.url import parse_name_and_version, substitute_version
from spack.url import strip_name_suffixes, strip_version_suffixes
from spack.url import UndetectableVersionError
from spack.version import Version


@pytest.mark.parametrize('url,expected', [
    # No suffix
    ('rgb-1.0.6', 'rgb-1.0.6'),
    # Misleading prefix
    ('jpegsrc.v9b', 'jpegsrc.v9b'),
    ('turbolinux702', 'turbolinux702'),
    ('converge_install_2.3.16', 'converge_install_2.3.16'),
    # Download type - src
    ('apache-ant-1.9.7-src', 'apache-ant-1.9.7'),
    ('go1.7.4.src', 'go1.7.4'),
    # Download type - source
    ('bowtie2-2.2.5-source', 'bowtie2-2.2.5'),
    ('grib_api-1.17.0-Source', 'grib_api-1.17.0'),
    # Download type - full
    ('julia-0.4.3-full', 'julia-0.4.3'),
    # Download type - bin
    ('apache-maven-3.3.9-bin', 'apache-maven-3.3.9'),
    # Download type - binary
    ('Jmol-14.8.0-binary', 'Jmol-14.8.0'),
    # Download type - gem
    ('rubysl-date-2.0.9.gem', 'rubysl-date-2.0.9'),
    # Download type - tar
    ('gromacs-4.6.1-tar', 'gromacs-4.6.1'),
    # Download type - sh
    ('Miniconda2-4.3.11-Linux-x86_64.sh', 'Miniconda2-4.3.11'),
    # Download version - release
    ('v1.0.4-release', 'v1.0.4'),
    # Download version - stable
    ('libevent-2.0.21-stable', 'libevent-2.0.21'),
    # Download version - final
    ('2.6.7-final', '2.6.7'),
    # Download version - rel
    ('v1.9.5.1rel', 'v1.9.5.1'),
    # Download version - orig
    ('dash_0.5.5.1.orig', 'dash_0.5.5.1'),
    # Download version - plus
    ('ncbi-blast-2.6.0+-src', 'ncbi-blast-2.6.0'),
    # License
    ('cppad-20170114.gpl', 'cppad-20170114'),
    # Arch
    ('pcraster-4.1.0_x86-64', 'pcraster-4.1.0'),
    # OS - linux
    ('astyle_2.04_linux', 'astyle_2.04'),
    # OS - unix
    ('install-tl-unx', 'install-tl'),
    # OS - macos
    ('astyle_1.23_macosx', 'astyle_1.23'),
    ('haxe-2.08-osx', 'haxe-2.08'),
    # PyPI - wheel
    ('entrypoints-0.2.2-py2.py3-none-any.whl', 'entrypoints-0.2.2'),
    ('numpy-1.12.0-cp27-cp27m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl', 'numpy-1.12.0'),  # noqa
    # PyPI - exe
    ('PyYAML-3.12.win-amd64-py3.5.exe', 'PyYAML-3.12'),
    # Combinations of multiple patterns - all
    ('p7zip_9.04_src_all', 'p7zip_9.04'),
    # Combinations of multiple patterns - run
    ('cuda_8.0.44_linux.run', 'cuda_8.0.44'),
    # Combinations of multiple patterns - file
    ('ack-2.14-single-file', 'ack-2.14'),
    # Combinations of multiple patterns - jar
    ('antlr-3.4-complete.jar', 'antlr-3.4'),
    # Combinations of multiple patterns - oss
    ('tbb44_20160128oss_src_0', 'tbb44_20160128'),
    # Combinations of multiple patterns - darwin
    ('ghc-7.0.4-x86_64-apple-darwin', 'ghc-7.0.4'),
    ('ghc-7.0.4-i386-apple-darwin', 'ghc-7.0.4'),
    # Combinations of multiple patterns - arch
    ('VizGlow_v2.2alpha17-R21November2016-Linux-x86_64-Install',
     'VizGlow_v2.2alpha17-R21November2016'),
    ('jdk-8u92-linux-x64', 'jdk-8u92'),
    ('cuda_6.5.14_linux_64.run', 'cuda_6.5.14'),
    # Combinations of multiple patterns - with
    ('mafft-7.221-with-extensions-src', 'mafft-7.221'),
    ('spark-2.0.0-bin-without-hadoop', 'spark-2.0.0'),
    # Combinations of multiple patterns - public
    ('dakota-6.3-public.src', 'dakota-6.3'),
    # Combinations of multiple patterns - universal
    ('synergy-1.3.6p2-MacOSX-Universal', 'synergy-1.3.6p2'),
    # Combinations of multiple patterns - dynamic
    ('snptest_v2.5.2_linux_x86_64_dynamic', 'snptest_v2.5.2'),
])
def test_url_strip_version_suffixes(url, expected):
    stripped = strip_version_suffixes(url)
    assert stripped == expected


@pytest.mark.parametrize('url,version,expected', [
    # No suffix
    ('rgb-1.0.6', '1.0.6', 'rgb'),
    ('nauty26r7', '26r7', 'nauty'),
    # Download type - install
    ('converge_install_2.3.16', '2.3.16', 'converge'),
    # Download type - src
    ('jpegsrc.v9b', '9b', 'jpeg'),
    # Download type - archive
    ('coinhsl-archive-2014.01.17', '2014.01.17', 'coinhsl'),
    # Download type - std
    ('ghostscript-fonts-std-8.11', '8.11', 'ghostscript-fonts'),
    # Download version - release
    ('cbench_release_1.3.0.tar.gz', '1.3.0', 'cbench'),
    # Download version - snapshot
    ('gts-snapshot-121130', '121130', 'gts'),
    # Download version - distrib
    ('zoltan_distrib_v3.83', '3.83', 'zoltan'),
    # VCS - bazaar
    ('libvterm-0+bzr681', '681', 'libvterm'),
    # License - gpl
    ('PyQt-x11-gpl-4.11.3', '4.11.3', 'PyQt-x11')
])
def test_url_strip_name_suffixes(url, version, expected):
    stripped = strip_name_suffixes(url, version)
    assert stripped == expected


@pytest.mark.parametrize('name,noffset,ver,voffset,path', [
    # Name in path
    ('antlr', 25, '2.7.7', 40, 'https://github.com/antlr/antlr/tarball/v2.7.7'),
    # Name in stem
    ('gmp', 32, '6.0.0a', 36, 'https://gmplib.org/download/gmp/gmp-6.0.0a.tar.bz2'),
    # Name in suffix

    # Don't think I've ever seen one of these before
    # We don't look for it, so it would probably fail anyway

    # Version in path
    ('nextflow', 31, '0.20.1', 59, 'https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow'),
    # Version in stem
    ('zlib', 24, '1.2.10', 29, 'http://zlib.net/fossils/zlib-1.2.10.tar.gz'),
    ('slepc', 51, '3.6.2', 57, 'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz'),
    ('cloog', 61, '0.18.1', 67, 'http://www.bastoul.net/cloog/pages/download/count.php3?url=./cloog-0.18.1.tar.gz'),
    ('libxc', 58, '2.2.2', 64, 'http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz'),
    # Version in suffix
    ('swiftsim', 36, '0.3.0', 76, 'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0'),
    ('swiftsim', 55, '0.3.0', 95, 'https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0'),
    ('sionlib', 30, '1.7.1', 59, 'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1'),
    # Regex in name
    ('voro++', 40, '0.4.6', 47, 'http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz'),
    # SourceForge download
    ('glew', 55, '2.0.0', 60, 'https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download'),
])
def test_url_parse_offset(name, noffset, ver, voffset, path):
    """Tests that the name, version and offsets are computed correctly.

    Args:
        name (str): expected name
        noffset (int): name offset
        ver (str): expected version
        voffset (int): version offset
        path (str): url to be parsed
    """
    # Make sure parse_name_offset and parse_name_version are working
    v, vstart, vlen, vi, vre = parse_version_offset(path)
    n, nstart, nlen, ni, nre = parse_name_offset(path, v)

    assert n == name
    assert v == ver
    assert nstart == noffset
    assert vstart == voffset


@pytest.mark.parametrize('name,version,url', [
    # Common Repositories - github downloads

    ('nco', '4.6.2', 'https://github.com/nco/nco/archive/4.6.2.tar.gz'),
    # name/archive/vver.ver
    ('vim', '8.0.0134', 'https://github.com/vim/vim/archive/v8.0.0134.tar.gz'),
    # name/archive/name-ver.ver
    ('oce', '0.18', 'https://github.com/tpaviot/oce/archive/OCE-0.18.tar.gz'),
    # name/releases/download/vver/name-ver.ver
    ('libmesh', '1.0.0', 'https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2'),
    # name/tarball/vver.ver
    ('git', '2.7.1', 'https://github.com/git/git/tarball/v2.7.1'),
    # name/zipball/vver.ver
    ('git', '2.7.1', 'https://github.com/git/git/zipball/v2.7.1'),

    # Common Repositories - gitlab downloads

    # name/repository/archive.ext?ref=vver.ver
    ('swiftsim', '0.3.0',
     'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0'),
    # /api/v4/projects/NAMESPACE%2Fname/repository/archive.ext?sha=vver.ver
    ('swiftsim', '0.3.0',
     'https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0'),
    # name/repository/archive.ext?ref=name-ver.ver
    ('icet', '1.2.3',
     'https://gitlab.kitware.com/icet/icet/repository/archive.tar.gz?ref=IceT-1.2.3'),
    # /api/v4/projects/NAMESPACE%2Fname/repository/archive.ext?sha=name-ver.ver
    ('icet', '1.2.3',
     'https://gitlab.kitware.com/api/v4/projects/icet%2Ficet/repository/archive.tar.bz2?sha=IceT-1.2.3'),

    # Common Repositories - bitbucket downloads

    # name/get/ver.ver
    ('eigen', '3.2.7', 'https://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2'),
    # name/get/vver.ver
    ('hoomd-blue', '1.3.3',
     'https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2'),
    # name/downloads/name-ver.ver
    ('dolfin', '2016.1.0',
     'https://bitbucket.org/fenics-project/dolfin/downloads/dolfin-2016.1.0.tar.gz'),
    # Common Repositories - sourceforge downloads

    # name-ver.ver
    ('libpng', '1.6.27',
     'http://download.sourceforge.net/libpng/libpng-1.6.27.tar.gz'),
    ('lcms2', '2.6',
     'http://downloads.sourceforge.net/project/lcms/lcms/2.6/lcms2-2.6.tar.gz'),
    ('modules', '3.2.10',
     'http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz'),
    # name-ver.ver.ext/download
    ('glew', '2.0.0',
     'https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download'),

    # Common Repositories - cran downloads

    # name.name_ver.ver-ver.ver
    ('TH.data', '1.0-8', 'https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz'),
    ('knitr', '1.14', 'https://cran.rstudio.com/src/contrib/knitr_1.14.tar.gz'),
    ('devtools', '1.12.0', 'https://cloud.r-project.org/src/contrib/devtools_1.12.0.tar.gz'),

    # Common Repositories - pypi downloads

    # name.name_name-ver.ver
    ('3to2', '1.1.1', 'https://pypi.python.org/packages/source/3/3to2/3to2-1.1.1.zip'),
    ('mpmath', '0.19',
     'https://pypi.python.org/packages/source/m/mpmath/mpmath-all-0.19.tar.gz'),
    ('pandas', '0.16.0',
     'https://pypi.python.org/packages/source/p/pandas/pandas-0.16.0.tar.gz#md5=bfe311f05dc0c351f8955fbd1e296e73'),
    ('sphinx_rtd_theme', '0.1.10a0',
     'https://pypi.python.org/packages/da/6b/1b75f13d8aa3333f19c6cdf1f0bc9f52ea739cae464fbee050307c121857/sphinx_rtd_theme-0.1.10a0.tar.gz'),
    ('backports.ssl_match_hostname', '3.5.0.1',
     'https://pypi.io/packages/source/b/backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz'),
    # Common Repositories - bazaar downloads
    ('libvterm', '681', 'http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr681.tar.gz'),

    # Common Tarball Formats

    # ver.ver
    ('eigen', '3.2.7', 'https://bitbucket.org/eigen/eigen/get/3.2.7.tar.bz2'),
    # ver.ver-ver
    ('ImageMagick', '7.0.2-7', 'https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz'),
    # vver.ver
    ('CGNS', '3.3.0', 'https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz'),
    # vver_ver
    ('luafilesystem', '1_6_3', 'https://github.com/keplerproject/luafilesystem/archive/v1_6_3.tar.gz'),

    # No separators
    ('turbolinux', '702', 'file://{0}/turbolinux702.tar.gz'.format(os.getcwd())),
    ('nauty', '26r7', 'http://pallini.di.uniroma1.it/nauty26r7.tar.gz'),
    # Dashes only
    ('Trilinos', '12-10-1',
     'https://github.com/trilinos/Trilinos/archive/trilinos-release-12-10-1.tar.gz'),
    ('panda', '2016-03-07',
     'http://comopt.ifi.uni-heidelberg.de/software/PANDA/downloads/panda-2016-03-07.tar'),
    ('gts', '121130',
     'http://gts.sourceforge.net/tarballs/gts-snapshot-121130.tar.gz'),
    ('cdd', '061a',
     'http://www.cs.mcgill.ca/~fukuda/download/cdd/cdd-061a.tar.gz'),
    # Only underscores
    ('tinyxml', '2_6_2',
     'https://sourceforge.net/projects/tinyxml/files/tinyxml/2.6.2/tinyxml_2_6_2.tar.gz'),
    ('boost', '1_55_0',
     'http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2'),
    ('yorick', '2_2_04',
     'https://github.com/dhmunro/yorick/archive/y_2_2_04.tar.gz'),
    ('tbb', '44_20160413',
     'https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20160413oss_src.tgz'),

    # Only dots

    # name.name.ver.ver
    ('prank', '150803', 'http://wasabiapp.org/download/prank/prank.source.150803.tgz'),
    ('jpeg', '9b', 'http://www.ijg.org/files/jpegsrc.v9b.tar.gz'),
    ('openjpeg', '2.1',
     'https://github.com/uclouvain/openjpeg/archive/version.2.1.tar.gz'),
    # name.namever.ver
    ('atlas', '3.11.34',
     'http://sourceforge.net/projects/math-atlas/files/Developer%20%28unstable%29/3.11.34/atlas3.11.34.tar.bz2'),
    ('visit', '2.10.1', 'http://portal.nersc.gov/project/visit/releases/2.10.1/visit2.10.1.tar.gz'),
    ('geant', '4.10.01.p03', 'http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz'),
    ('tcl', '8.6.5', 'http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz'),

    # Dash and dots

    # name-name-ver.ver
    # digit in name
    ('m4', '1.4.17', 'https://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz'),
    # letter in version
    ('gmp', '6.0.0a', 'https://gmplib.org/download/gmp/gmp-6.0.0a.tar.bz2'),
    # version starts with 'v'
    ('LaunchMON', '1.0.2',
     'https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz'),
    # name-ver-ver.ver
    ('libedit', '20150325-3.1', 'http://thrysoee.dk/editline/libedit-20150325-3.1.tar.gz'),

    # Dash and unserscores

    # name-name-ver_ver
    ('icu4c', '57_1', 'http://download.icu-project.org/files/icu4c/57.1/icu4c-57_1-src.tgz'),

    # Underscores and dots

    # name_name_ver.ver
    ('superlu_dist', '4.1', 'http://crd-legacy.lbl.gov/~xiaoye/SuperLU/superlu_dist_4.1.tar.gz'),
    ('pexsi', '0.9.0', 'https://math.berkeley.edu/~linlin/pexsi/download/pexsi_v0.9.0.tar.gz'),
    # name_name.ver.ver
    ('fer', '696', 'ftp://ftp.pmel.noaa.gov/ferret/pub/source/fer_source.v696.tar.gz'),

    # Dash dot dah dot

    # name-name-ver.ver-ver.ver
    ('sowing', '1.1.23-p1', 'http://ftp.mcs.anl.gov/pub/petsc/externalpackages/sowing-1.1.23-p1.tar.gz'),
    ('bib2xhtml', '3.0-15-gf506', 'http://www.spinellis.gr/sw/textproc/bib2xhtml/bib2xhtml-v3.0-15-gf506.tar.gz'),
    # namever.ver-ver.ver
    ('go', '1.4-bootstrap-20161024', 'https://storage.googleapis.com/golang/go1.4-bootstrap-20161024.tar.gz'),

    # Underscore dash dot

    # name_name-ver.ver
    ('the_silver_searcher', '0.32.0', 'http://geoff.greer.fm/ag/releases/the_silver_searcher-0.32.0.tar.gz'),
    ('sphinx_rtd_theme', '0.1.10a0',
     'https://pypi.python.org/packages/source/s/sphinx_rtd_theme/sphinx_rtd_theme-0.1.10a0.tar.gz'),

    # Dot underscore dot dash dot

    # name.name_ver.ver-ver.ver
    ('TH.data', '1.0-8', 'https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz'),
    ('XML', '3.98-1.4', 'https://cran.r-project.org/src/contrib/XML_3.98-1.4.tar.gz'),

    # Dash dot underscore dot

    # name-name-ver.ver_ver.ver
    ('pypar', '2.1.5_108',
     'https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-2.1.5_108.tgz'),
    # name-namever.ver_ver.ver
    ('STAR-CCM+', '11.06.010_02',
     'file://{0}/STAR-CCM+11.06.010_02_linux-x86_64.tar.gz'.format(os.getcwd())),

    # Weird URLS

    # github.com/repo/name/releases/download/name-vver/name
    ('nextflow', '0.20.1', 'https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow'),
    # suffix queries
    ('swiftsim', '0.3.0', 'http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0'),
    ('swiftsim', '0.3.0', 'https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0'),
    ('sionlib', '1.7.1', 'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1'),
    # stem queries
    ('slepc', '3.6.2', 'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz'),
    ('otf', '1.12.5salmon',
     'http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz'),
    # single character name
    ('R', '3.3.2', 'https://cloud.r-project.org/src/base/R-3/R-3.3.2.tar.gz'),
    # name starts with digit
    ('3to2', '1.1.1', 'https://pypi.python.org/packages/source/3/3to2/3to2-1.1.1.zip'),
    # plus in name
    ('gtk+', '2.24.31', 'http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.31.tar.xz'),
    ('voro++', '0.4.6', 'http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz'),
    # Name comes before download.php
    ('sionlib', '1.7.1', 'http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1'),
    # Ignore download.php
    ('slepc', '3.6.2', 'http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz'),
    ('ScientificPython', '2.8.1',
     'https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz'),
    # gloox beta style
    ('gloox', '1.0-beta7', 'http://camaya.net/download/gloox-1.0-beta7.tar.bz2'),
    # sphinx beta style
    ('sphinx', '1.10-beta', 'http://sphinxsearch.com/downloads/sphinx-1.10-beta.tar.gz'),
    # ruby version style
    ('ruby', '1.9.1-p243', 'ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.1-p243.tar.gz'),
    # rc style
    ('libvorbis', '1.2.2rc1', 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.2.2rc1.tar.bz2'),
    # dash rc style
    ('js', '1.8.0-rc1', 'http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz'),
    # apache version style
    ('apache-cassandra', '1.2.0-rc2',
     'http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin.tar.gz'),
    # xaw3d version
    ('Xaw3d', '1.5E', 'ftp://ftp.visi.com/users/hawkeyd/X/Xaw3d-1.5E.tar.gz'),
    # fann version
    ('fann', '2.1.0beta', 'http://downloads.sourceforge.net/project/fann/fann/2.1.0beta/fann-2.1.0beta.zip'),
    # imap version
    ('imap', '2007f', 'ftp://ftp.cac.washington.edu/imap/imap-2007f.tar.gz'),
    # suite3270 version
    ('suite3270', '3.3.12ga7',
     'http://sourceforge.net/projects/x3270/files/x3270/3.3.12ga7/suite3270-3.3.12ga7-src.tgz'),
    # scalasca version
    ('cube', '4.2.3', 'http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-4.2.3.tar.gz'),
    ('cube', '4.3-TP1', 'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz'),
    # github raw url
    ('CLAMR', '2.0.7', 'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true'),
    # luaposix version
    ('luaposix', '33.4.0', 'https://github.com/luaposix/luaposix/archive/release-v33.4.0.tar.gz'),
    # nco version
    ('nco', '4.6.2-beta03', 'https://github.com/nco/nco/archive/4.6.2-beta03.tar.gz'),
    ('nco', '4.6.3-alpha04', 'https://github.com/nco/nco/archive/4.6.3-alpha04.tar.gz'),
])
def test_url_parse_name_and_version(name, version, url):
    # Make sure correct name and version are extracted.
    parsed_name, parsed_version = parse_name_and_version(url)
    assert parsed_name == name
    assert parsed_version == Version(version)

    # Make sure Spack formulates the right URL when we try to
    # build one with a specific version.
    assert url == substitute_version(url, version)


@pytest.mark.parametrize('not_detectable_url', [
    'http://www.netlib.org/blas/blast-forum/cblas.tgz',
    'http://www.netlib.org/voronoi/triangle.zip',
])
def test_no_version(not_detectable_url):
    with pytest.raises(UndetectableVersionError):
        parse_name_and_version(not_detectable_url)
