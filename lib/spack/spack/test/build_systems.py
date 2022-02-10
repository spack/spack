# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

import pytest

import llnl.util.filesystem as fs

import spack.environment
import spack.repo
from spack.build_environment import ChildError, get_std_cmake_args, setup_package
from spack.spec import Spec
from spack.util.executable import which

DATA_PATH = os.path.join(spack.paths.test_path, 'data')


@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'make', 'affirmative', '*'))
)
def test_affirmative_make_check(directory, config, mock_packages, working_env):
    """Tests that Spack correctly detects targets in a Makefile."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with fs.working_dir(directory):
        assert pkg._has_make_target('check')

        pkg._if_make_target_execute('check')


@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'make', 'negative', '*'))
)
@pytest.mark.regression('9067')
def test_negative_make_check(directory, config, mock_packages, working_env):
    """Tests that Spack correctly ignores false positives in a Makefile."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with fs.working_dir(directory):
        assert not pkg._has_make_target('check')

        pkg._if_make_target_execute('check')


@pytest.mark.skipif(not which('ninja'), reason='ninja is not installed')
@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'ninja', 'affirmative', '*'))
)
def test_affirmative_ninja_check(
        directory, config, mock_packages, working_env):
    """Tests that Spack correctly detects targets in a Ninja build script."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with fs.working_dir(directory):
        assert pkg._has_ninja_target('check')

        pkg._if_ninja_target_execute('check')

        # Clean up Ninja files
        for filename in glob.iglob('.ninja_*'):
            os.remove(filename)


@pytest.mark.skipif(not which('ninja'), reason='ninja is not installed')
@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'ninja', 'negative', '*'))
)
def test_negative_ninja_check(directory, config, mock_packages, working_env):
    """Tests that Spack correctly ignores false positives in a Ninja
    build script."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with fs.working_dir(directory):
        assert not pkg._has_ninja_target('check')

        pkg._if_ninja_target_execute('check')


def test_cmake_std_args(config, mock_packages):
    # Call the function on a CMakePackage instance
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    assert pkg.std_cmake_args == get_std_cmake_args(pkg)

    # Call it on another kind of package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    assert get_std_cmake_args(pkg)


def test_cmake_bad_generator(config, mock_packages):
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.generator = 'Yellow Sticky Notes'
    with pytest.raises(spack.package.InstallError):
        get_std_cmake_args(pkg)


def test_cmake_secondary_generator(config, mock_packages):
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.generator = 'CodeBlocks - Unix Makefiles'
    assert get_std_cmake_args(pkg)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestAutotoolsPackage(object):

    def test_with_or_without(self):
        s = Spec('a')
        s.concretize()
        pkg = spack.repo.get(s)

        options = pkg.with_or_without('foo')

        # Ensure that values that are not representing a feature
        # are not used by with_or_without
        assert '--without-none' not in options
        assert '--with-bar' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        def activate(value):
            return 'something'

        options = pkg.with_or_without('foo', activation_value=activate)
        assert '--without-none' not in options
        assert '--with-bar=something' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        options = pkg.enable_or_disable('foo')
        assert '--disable-none' not in options
        assert '--enable-bar' in options
        assert '--disable-baz' in options
        assert '--disable-fee' in options

        options = pkg.with_or_without('bvv')
        assert '--with-bvv' in options

        options = pkg.with_or_without('lorem-ipsum', variant='lorem_ipsum')
        assert '--without-lorem-ipsum' in options

    def test_none_is_allowed(self):
        s = Spec('a foo=none')
        s.concretize()
        pkg = spack.repo.get(s)

        options = pkg.with_or_without('foo')

        # Ensure that values that are not representing a feature
        # are not used by with_or_without
        assert '--with-none' not in options
        assert '--without-bar' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

    def test_libtool_archive_files_are_deleted_by_default(
            self, mutable_database
    ):
        # Install a package that creates a mock libtool archive
        s = Spec('libtool-deletion')
        s.concretize()
        s.package.do_install(explicit=True)

        # Assert the libtool archive is not there and we have
        # a log of removed files
        assert not os.path.exists(s.package.libtool_archive_file)
        search_directory = os.path.join(s.prefix, '.spack')
        libtool_deletion_log = fs.find(
            search_directory, 'removed_la_files.txt', recursive=True
        )
        assert libtool_deletion_log

    def test_libtool_archive_files_might_be_installed_on_demand(
            self, mutable_database, monkeypatch
    ):
        # Install a package that creates a mock libtool archive,
        # patch its package to preserve the installation
        s = Spec('libtool-deletion')
        s.concretize()
        monkeypatch.setattr(s.package, 'install_libtool_archives', True)
        s.package.do_install(explicit=True)

        # Assert libtool archives are installed
        assert os.path.exists(s.package.libtool_archive_file)

    def test_autotools_gnuconfig_replacement(self, mutable_database):
        """
        Tests whether only broken config.sub and config.guess are replaced with
        files from working alternatives from the gnuconfig package.
        """
        s = Spec('autotools-config-replacement +patch_config_files +gnuconfig')
        s.concretize()
        s.package.do_install()

        with open(os.path.join(s.prefix.broken, 'config.sub')) as f:
            assert "gnuconfig version of config.sub" in f.read()

        with open(os.path.join(s.prefix.broken, 'config.guess')) as f:
            assert "gnuconfig version of config.guess" in f.read()

        with open(os.path.join(s.prefix.working, 'config.sub')) as f:
            assert "gnuconfig version of config.sub" not in f.read()

        with open(os.path.join(s.prefix.working, 'config.guess')) as f:
            assert "gnuconfig version of config.guess" not in f.read()

    def test_autotools_gnuconfig_replacement_disabled(self, mutable_database):
        """
        Tests whether disabling patch_config_files
        """
        s = Spec('autotools-config-replacement ~patch_config_files +gnuconfig')
        s.concretize()
        s.package.do_install()

        with open(os.path.join(s.prefix.broken, 'config.sub')) as f:
            assert "gnuconfig version of config.sub" not in f.read()

        with open(os.path.join(s.prefix.broken, 'config.guess')) as f:
            assert "gnuconfig version of config.guess" not in f.read()

        with open(os.path.join(s.prefix.working, 'config.sub')) as f:
            assert "gnuconfig version of config.sub" not in f.read()

        with open(os.path.join(s.prefix.working, 'config.guess')) as f:
            assert "gnuconfig version of config.guess" not in f.read()

    @pytest.mark.disable_clean_stage_check
    def test_autotools_gnuconfig_replacement_no_gnuconfig(self, mutable_database):
        """
        Tests whether a useful error message is shown when patch_config_files is
        enabled, but gnuconfig is not listed as a direct build dependency.
        """
        s = Spec('autotools-config-replacement +patch_config_files ~gnuconfig')
        s.concretize()

        msg = "Cannot patch config files: missing dependencies: gnuconfig"
        with pytest.raises(ChildError, match=msg):
            s.package.do_install()

    @pytest.mark.disable_clean_stage_check
    def test_broken_external_gnuconfig(self, mutable_database, tmpdir):
        """
        Tests whether we get a useful error message when gnuconfig is marked
        external, but the install prefix is misconfigured and no config.guess
        and config.sub substitute files are found in the provided prefix.
        """
        env_dir = str(tmpdir.ensure('env', dir=True))
        gnuconfig_dir = str(tmpdir.ensure('gnuconfig', dir=True))  # empty dir
        with open(os.path.join(env_dir, 'spack.yaml'), 'w') as f:
            f.write("""\
spack:
  specs:
  - 'autotools-config-replacement +patch_config_files +gnuconfig'
  packages:
    gnuconfig:
      buildable: false
      externals:
      - spec: gnuconfig@1.0.0
        prefix: {0}
""".format(gnuconfig_dir))

        msg = ("Spack could not find `config.guess`.*misconfigured as an "
               "external package")
        with spack.environment.Environment(env_dir) as e:
            e.concretize()
            with pytest.raises(ChildError, match=msg):
                e.install_all()


@pytest.mark.usefixtures('config', 'mock_packages')
class TestCMakePackage(object):

    def test_define(self):
        s = Spec('cmake-client')
        s.concretize()
        pkg = spack.repo.get(s)

        for cls in (list, tuple):
            arg = pkg.define('MULTI', cls(['right', 'up']))
            assert arg == '-DMULTI:STRING=right;up'

        arg = pkg.define('MULTI', fs.FileList(['/foo', '/bar']))
        assert arg == '-DMULTI:STRING=/foo;/bar'

        arg = pkg.define('ENABLE_TRUTH', False)
        assert arg == '-DENABLE_TRUTH:BOOL=OFF'
        arg = pkg.define('ENABLE_TRUTH', True)
        assert arg == '-DENABLE_TRUTH:BOOL=ON'

        arg = pkg.define('SINGLE', 'red')
        assert arg == '-DSINGLE:STRING=red'

    def test_define_from_variant(self):
        s = Spec('cmake-client multi=up,right ~truthy single=red')
        s.concretize()
        pkg = spack.repo.get(s)

        arg = pkg.define_from_variant('MULTI')
        assert arg == '-DMULTI:STRING=right;up'

        arg = pkg.define_from_variant('ENABLE_TRUTH', 'truthy')
        assert arg == '-DENABLE_TRUTH:BOOL=OFF'

        arg = pkg.define_from_variant('SINGLE')
        assert arg == '-DSINGLE:STRING=red'

        with pytest.raises(KeyError, match="not a variant"):
            pkg.define_from_variant('NONEXISTENT')


@pytest.mark.usefixtures('config', 'mock_packages')
class TestGNUMirrorPackage(object):

    def test_define(self):
        s = Spec('mirror-gnu')
        s.concretize()
        pkg = spack.repo.get(s)

        s = Spec('mirror-gnu-broken')
        s.concretize()
        pkg_broken = spack.repo.get(s)

        cls_name = type(pkg_broken).__name__
        with pytest.raises(AttributeError,
                           match=r'{0} must define a `gnu_mirror_path` '
                                 r'attribute \[none defined\]'
                                 .format(cls_name)):
            pkg_broken.urls

        assert pkg.urls[0] == 'https://ftpmirror.gnu.org/' \
                              'make/make-4.2.1.tar.gz'


@pytest.mark.usefixtures('config', 'mock_packages')
class TestSourceforgePackage(object):

    def test_define(self):
        s = Spec('mirror-sourceforge')
        s.concretize()
        pkg = spack.repo.get(s)

        s = Spec('mirror-sourceforge-broken')
        s.concretize()
        pkg_broken = spack.repo.get(s)

        cls_name = type(pkg_broken).__name__
        with pytest.raises(AttributeError,
                           match=r'{0} must define a `sourceforge_mirror_path`'
                                 r' attribute \[none defined\]'
                                 .format(cls_name)):
            pkg_broken.urls

        assert pkg.urls[0] == 'https://prdownloads.sourceforge.net/' \
                              'tcl/tcl8.6.5-src.tar.gz'


@pytest.mark.usefixtures('config', 'mock_packages')
class TestSourcewarePackage(object):

    def test_define(self):
        s = Spec('mirror-sourceware')
        s.concretize()
        pkg = spack.repo.get(s)

        s = Spec('mirror-sourceware-broken')
        s.concretize()
        pkg_broken = spack.repo.get(s)

        cls_name = type(pkg_broken).__name__
        with pytest.raises(AttributeError,
                           match=r'{0} must define a `sourceware_mirror_path` '
                                 r'attribute \[none defined\]'
                                 .format(cls_name)):
            pkg_broken.urls

        assert pkg.urls[0] == 'https://sourceware.org/pub/' \
                              'bzip2/bzip2-1.0.8.tar.gz'


@pytest.mark.usefixtures('config', 'mock_packages')
class TestXorgPackage(object):

    def test_define(self):
        s = Spec('mirror-xorg')
        s.concretize()
        pkg = spack.repo.get(s)

        s = Spec('mirror-xorg-broken')
        s.concretize()
        pkg_broken = spack.repo.get(s)

        cls_name = type(pkg_broken).__name__
        with pytest.raises(AttributeError,
                           match=r'{0} must define a `xorg_mirror_path` '
                                 r'attribute \[none defined\]'
                                 .format(cls_name)):
            pkg_broken.urls

        assert pkg.urls[0] == 'https://www.x.org/archive/individual/' \
                              'util/util-macros-1.19.1.tar.bz2'


def test_cmake_define_from_variant_conditional(config, mock_packages):
    """Test that define_from_variant returns empty string when a condition on a variant
    is not met. When this is the case, the variant is not set in the spec."""
    s = Spec('cmake-conditional-variants-test').concretized()
    assert 'example' not in s.variants
    assert s.package.define_from_variant('EXAMPLE', 'example') == ''


def test_autotools_args_from_conditional_variant(config, mock_packages):
    """Test that _activate_or_not returns an empty string when a condition on a variant
    is not met. When this is the case, the variant is not set in the spec."""
    s = Spec('autotools-conditional-variants-test').concretized()
    assert 'example' not in s.variants
    assert len(s.package._activate_or_not('example', 'enable', 'disable')) == 0
