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
import os.path
import pytest

import spack.repo
from spack.paths import mock_packages_path
from spack.util.naming import mod_to_class
from spack.spec import Spec
from spack.util.package_hash import package_content


@pytest.mark.usefixtures('config', 'mock_packages')
class TestPackage(object):
    def test_load_package(self):
        spack.repo.get('mpich')

    def test_package_name(self):
        pkg = spack.repo.get('mpich')
        assert pkg.name == 'mpich'

    def test_package_filename(self):
        repo = spack.repo.Repo(mock_packages_path)
        filename = repo.filename_for_package_name('mpich')
        assert filename == os.path.join(
            mock_packages_path,
            'packages',
            'mpich',
            'package.py'
        )

    def test_nonexisting_package_filename(self):
        repo = spack.repo.Repo(mock_packages_path)
        filename = repo.filename_for_package_name('some-nonexisting-package')
        assert filename == os.path.join(
            mock_packages_path,
            'packages',
            'some-nonexisting-package',
            'package.py'
        )

    def test_package_class_names(self):
        assert 'Mpich' == mod_to_class('mpich')
        assert 'PmgrCollective' == mod_to_class('pmgr_collective')
        assert 'PmgrCollective' == mod_to_class('pmgr-collective')
        assert 'Pmgrcollective' == mod_to_class('PmgrCollective')
        assert '_3db' == mod_to_class('3db')

    def test_content_hash_all_same_but_patch_contents(self):
        spec1 = Spec("hash-test1@1.1")
        spec2 = Spec("hash-test2@1.1")
        spec1.concretize()
        spec2.concretize()
        content1 = package_content(spec1)
        content1 = content1.replace(spec1.package.__class__.__name__, '')
        content2 = package_content(spec2)
        content2 = content2.replace(spec2.package.__class__.__name__, '')
        assert spec1.package.content_hash(content=content1) != \
            spec2.package.content_hash(content=content2)

    def test_content_hash_different_variants(self):
        spec1 = Spec("hash-test1@1.2 +variantx")
        spec2 = Spec("hash-test2@1.2 ~variantx")
        spec1.concretize()
        spec2.concretize()
        content1 = package_content(spec1)
        content1 = content1.replace(spec1.package.__class__.__name__, '')
        content2 = package_content(spec2)
        content2 = content2.replace(spec2.package.__class__.__name__, '')
        assert spec1.package.content_hash(content=content1) == \
            spec2.package.content_hash(content=content2)

    def test_all_same_but_archive_hash(self):
        spec1 = Spec("hash-test1@1.3")
        spec2 = Spec("hash-test2@1.3")
        spec1.concretize()
        spec2.concretize()
        content1 = package_content(spec1)
        content1 = content1.replace(spec1.package.__class__.__name__, '')
        content2 = package_content(spec2)
        content2 = content2.replace(spec2.package.__class__.__name__, '')
        assert spec1.package.content_hash(content=content1) != \
            spec2.package.content_hash(content=content2)

    # Below tests target direct imports of spack packages from the
    # spack.pkg namespace
    def test_import_package(self):
        import spack.pkg.builtin.mock.mpich             # noqa

    def test_import_package_as(self):
        import spack.pkg.builtin.mock.mpich as mp       # noqa

        import spack.pkg.builtin.mock                   # noqa
        import spack.pkg.builtin.mock as m              # noqa
        from spack.pkg.builtin import mock              # noqa

    def test_inheritance_of_diretives(self):
        p = spack.repo.get('simple-inheritance')

        # Check dictionaries that should have been filled by directives
        assert len(p.dependencies) == 3
        assert 'cmake' in p.dependencies
        assert 'openblas' in p.dependencies
        assert 'mpi' in p.dependencies
        assert len(p.provided) == 2

        # Check that Spec instantiation behaves as we expect
        s = Spec('simple-inheritance')
        s.concretize()
        assert '^cmake' in s
        assert '^openblas' in s
        assert '+openblas' in s
        assert 'mpi' in s

        s = Spec('simple-inheritance~openblas')
        s.concretize()
        assert '^cmake' in s
        assert '^openblas' not in s
        assert '~openblas' in s
        assert 'mpi' in s

    def test_dependency_extensions(self):
        s = Spec('extension2')
        s.concretize()
        deps = set(x.name for x in s.package.dependency_activations())
        assert deps == set(['extension1'])

    def test_import_class_from_package(self):
        from spack.pkg.builtin.mock.mpich import Mpich  # noqa

    def test_import_module_from_package(self):
        from spack.pkg.builtin.mock import mpich        # noqa

    def test_import_namespace_container_modules(self):
        import spack.pkg                                # noqa
        import spack.pkg as p                           # noqa
        from spack import pkg                           # noqa

        import spack.pkg.builtin                        # noqa
        import spack.pkg.builtin as b                   # noqa
        from spack.pkg import builtin                   # noqa

        import spack.pkg.builtin.mock                   # noqa
        import spack.pkg.builtin.mock as m              # noqa
        from spack.pkg.builtin import mock              # noqa

    @pytest.mark.regression('2737')
    def test_urls_for_versions(self):
        # Checks that a version directive without a 'url' argument
        # specified uses the default url
        for spec_str in ('url_override@0.9.0', 'url_override@1.0.0'):
            s = Spec(spec_str).concretized()
            url = s.package.url_for_version('0.9.0')
            assert url == 'http://www.anothersite.org/uo-0.9.0.tgz'

            url = s.package.url_for_version('1.0.0')
            assert url == 'http://www.doesnotexist.org/url_override-1.0.0.tar.gz'

            url = s.package.url_for_version('0.8.1')
            assert url == 'http://www.doesnotexist.org/url_override-0.8.1.tar.gz'
