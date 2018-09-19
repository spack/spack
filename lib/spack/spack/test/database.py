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
"""
These tests check the database is functioning properly,
both in memory and in its file
"""
import datetime
import functools
import multiprocessing
import os
import pytest

from llnl.util.tty.colify import colify

import spack.repo
import spack.store
from spack.test.conftest import MockPackageMultiRepo
from spack.util.executable import Executable


pytestmark = pytest.mark.db


@pytest.fixture()
def usr_folder_exists(monkeypatch):
    """The ``/usr`` folder is assumed to be existing in some tests. This
    fixture makes it such that its existence is mocked, so we have no
    requirements on the system running tests.
    """
    isdir = os.path.isdir

    @functools.wraps(os.path.isdir)
    def mock_isdir(path):
        if path == '/usr':
            return True
        return isdir(path)

    monkeypatch.setattr(os.path, 'isdir', mock_isdir)


def _print_ref_counts():
    """Print out all ref counts for the graph used here, for debugging"""
    recs = []

    def add_rec(spec):
        cspecs = spack.store.db.query(spec, installed=any)

        if not cspecs:
            recs.append("[ %-7s ] %-20s-" % ('', spec))
        else:
            key = cspecs[0].dag_hash()
            rec = spack.store.db.get_record(cspecs[0])
            recs.append("[ %-7s ] %-20s%d" % (key[:7], spec, rec.ref_count))

    with spack.store.db.read_transaction():
        add_rec('mpileaks ^mpich')
        add_rec('callpath ^mpich')
        add_rec('mpich')

        add_rec('mpileaks ^mpich2')
        add_rec('callpath ^mpich2')
        add_rec('mpich2')

        add_rec('mpileaks ^zmpi')
        add_rec('callpath ^zmpi')
        add_rec('zmpi')
        add_rec('fake')

        add_rec('dyninst')
        add_rec('libdwarf')
        add_rec('libelf')

    colify(recs, cols=3)


def _check_merkleiness():
    """Ensure the spack database is a valid merkle graph."""
    all_specs = spack.store.db.query(installed=any)

    seen = {}
    for spec in all_specs:
        for dep in spec.dependencies():
            hash_key = dep.dag_hash()
            if hash_key not in seen:
                seen[hash_key] = id(dep)
            else:
                assert seen[hash_key] == id(dep)


def _check_db_sanity(database):
    """Utiilty function to check db against install layout."""
    pkg_in_layout = sorted(spack.store.layout.all_specs())
    actual = sorted(database.query())

    externals = sorted([x for x in actual if x.external])
    nexpected = len(pkg_in_layout) + len(externals)

    assert nexpected == len(actual)

    non_external_in_db = sorted([x for x in actual if not x.external])

    for e, a in zip(pkg_in_layout, non_external_in_db):
        assert e == a

    _check_merkleiness()


def _check_remove_and_add_package(database, spec):
    """Remove a spec from the DB, then add it and make sure everything's
    still ok once it is added.  This checks that it was
    removed, that it's back when added again, and that ref
    counts are consistent.
    """
    original = database.query()
    database._check_ref_counts()

    # Remove spec
    concrete_spec = database.remove(spec)
    database._check_ref_counts()
    remaining = database.query()

    # ensure spec we removed is gone
    assert len(original) - 1 == len(remaining)
    assert all(s in original for s in remaining)
    assert concrete_spec not in remaining

    # add it back and make sure everything is ok.
    database.add(concrete_spec, spack.store.layout)
    installed = database.query()
    assert concrete_spec in installed
    assert installed == original

    # sanity check against direcory layout and check ref counts.
    _check_db_sanity(database)
    database._check_ref_counts()


def _mock_install(spec):
    s = spack.spec.Spec(spec)
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.do_install(fake=True)


def _mock_remove(spec):
    specs = spack.store.db.query(spec)
    assert len(specs) == 1
    spec = specs[0]
    spec.package.do_uninstall(spec)


def test_default_queries(database):
    # Testing a package whose name *doesn't* start with 'lib'
    # to ensure the library has 'lib' prepended to the name
    rec = database.get_record('zmpi')

    spec = rec.spec

    libraries = spec['zmpi'].libs
    assert len(libraries) == 1
    assert libraries.names[0] == 'zmpi'

    headers = spec['zmpi'].headers
    assert len(headers) == 1
    assert headers.names[0] == 'zmpi'

    command = spec['zmpi'].command
    assert isinstance(command, Executable)
    assert command.name == 'zmpi'
    assert os.path.exists(command.path)

    # Testing a package whose name *does* start with 'lib'
    # to ensure the library doesn't have a double 'lib' prefix
    rec = database.get_record('libelf')

    spec = rec.spec

    libraries = spec['libelf'].libs
    assert len(libraries) == 1
    assert libraries.names[0] == 'elf'

    headers = spec['libelf'].headers
    assert len(headers) == 1
    assert headers.names[0] == 'libelf'

    command = spec['libelf'].command
    assert isinstance(command, Executable)
    assert command.name == 'libelf'
    assert os.path.exists(command.path)


def test_005_db_exists(database):
    """Make sure db cache file exists after creating."""
    index_file = os.path.join(database.root, '.spack-db', 'index.json')
    lock_file = os.path.join(database.root, '.spack-db', 'lock')
    assert os.path.exists(str(index_file))
    assert os.path.exists(str(lock_file))


def test_010_all_install_sanity(database):
    """Ensure that the install layout reflects what we think it does."""
    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 14

    # Query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # Query specs with single configurations
    dyninst_specs = [s for s in all_specs if s.satisfies('dyninst')]
    libdwarf_specs = [s for s in all_specs if s.satisfies('libdwarf')]
    libelf_specs = [s for s in all_specs if s.satisfies('libelf')]

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^mpich')]
    ) == 1
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^mpich2')]
    ) == 1
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^zmpi')]
    ) == 1


def test_015_write_and_read(database):
    # write and read DB
    with spack.store.db.write_transaction():
        specs = spack.store.db.query()
        recs = [spack.store.db.get_record(s) for s in specs]

    for spec, rec in zip(specs, recs):
        new_rec = spack.store.db.get_record(spec)
        assert new_rec.ref_count == rec.ref_count
        assert new_rec.spec == rec.spec
        assert new_rec.path == rec.path
        assert new_rec.installed == rec.installed


def test_020_db_sanity(database):
    """Make sure query() returns what's actually in the db."""
    _check_db_sanity(database)


def test_025_reindex(database):
    """Make sure reindex works and ref counts are valid."""
    spack.store.store.reindex()
    _check_db_sanity(database)


def test_030_db_sanity_from_another_process(mutable_database):
    def read_and_modify():
        # check that other process can read DB
        _check_db_sanity(mutable_database)
        with mutable_database.write_transaction():
            _mock_remove('mpileaks ^zmpi')

    p = multiprocessing.Process(target=read_and_modify, args=())
    p.start()
    p.join()

    # ensure child process change is visible in parent process
    with mutable_database.read_transaction():
        assert len(mutable_database.query('mpileaks ^zmpi')) == 0


def test_040_ref_counts(database):
    """Ensure that we got ref counts right when we read the DB."""
    database._check_ref_counts()


def test_050_basic_query(database):
    """Ensure querying database is consistent with what is installed."""
    # query everything
    assert len(spack.store.db.query()) == 16

    # query specs with multiple configurations
    mpileaks_specs = database.query('mpileaks')
    callpath_specs = database.query('callpath')
    mpi_specs = database.query('mpi')

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # query specs with single configurations
    dyninst_specs = database.query('dyninst')
    libdwarf_specs = database.query('libdwarf')
    libelf_specs = database.query('libelf')

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(database.query('mpileaks ^mpich')) == 1
    assert len(database.query('mpileaks ^mpich2')) == 1
    assert len(database.query('mpileaks ^zmpi')) == 1

    # Query by date
    assert len(database.query(start_date=datetime.datetime.min)) == 16
    assert len(database.query(start_date=datetime.datetime.max)) == 0
    assert len(database.query(end_date=datetime.datetime.min)) == 0
    assert len(database.query(end_date=datetime.datetime.max)) == 16


def test_060_remove_and_add_root_package(database):
    _check_remove_and_add_package(database, 'mpileaks ^mpich')


def test_070_remove_and_add_dependency_package(database):
    _check_remove_and_add_package(database, 'dyninst')


def test_080_root_ref_counts(database):
    rec = database.get_record('mpileaks ^mpich')

    # Remove a top-level spec from the DB
    database.remove('mpileaks ^mpich')

    # record no longer in DB
    assert database.query('mpileaks ^mpich', installed=any) == []

    # record's deps have updated ref_counts
    assert database.get_record('callpath ^mpich').ref_count == 0
    assert database.get_record('mpich').ref_count == 1

    # Put the spec back
    database.add(rec.spec, spack.store.layout)

    # record is present again
    assert len(database.query('mpileaks ^mpich', installed=any)) == 1

    # dependencies have ref counts updated
    assert database.get_record('callpath ^mpich').ref_count == 1
    assert database.get_record('mpich').ref_count == 2


def test_090_non_root_ref_counts(database):
    database.get_record('mpileaks ^mpich')
    database.get_record('callpath ^mpich')

    # "force remove" a non-root spec from the DB
    database.remove('callpath ^mpich')

    # record still in DB but marked uninstalled
    assert database.query('callpath ^mpich', installed=True) == []
    assert len(database.query('callpath ^mpich', installed=any)) == 1

    # record and its deps have same ref_counts
    assert database.get_record(
        'callpath ^mpich', installed=any
    ).ref_count == 1
    assert database.get_record('mpich').ref_count == 2

    # remove only dependent of uninstalled callpath record
    database.remove('mpileaks ^mpich')

    # record and parent are completely gone.
    assert database.query('mpileaks ^mpich', installed=any) == []
    assert database.query('callpath ^mpich', installed=any) == []

    # mpich ref count updated properly.
    mpich_rec = database.get_record('mpich')
    assert mpich_rec.ref_count == 0


def test_100_no_write_with_exception_on_remove(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_remove('mpileaks ^zmpi')
            raise Exception()

    with database.read_transaction():
        assert len(database.query('mpileaks ^zmpi', installed=any)) == 1

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure zmpi is still there.
    with database.read_transaction():
        assert len(database.query('mpileaks ^zmpi', installed=any)) == 1


def test_110_no_write_with_exception_on_install(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_install('cmake')
            raise Exception()

    with database.read_transaction():
        assert database.query('cmake', installed=any) == []

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure cmake was not written.
    with database.read_transaction():
        assert database.query('cmake', installed=any) == []


def test_115_reindex_with_packages_not_in_repo(mutable_database):
    # Dont add any package definitions to this repository, the idea is that
    # packages should not have to be defined in the repository once they
    # are installed
    with spack.repo.swap(MockPackageMultiRepo([])):
        spack.store.store.reindex()
        _check_db_sanity(mutable_database)


def test_external_entries_in_db(database):
    rec = database.get_record('mpileaks ^zmpi')
    assert rec.spec.external_path is None
    assert rec.spec.external_module is None

    rec = database.get_record('externaltool')
    assert rec.spec.external_path == '/path/to/external_tool'
    assert rec.spec.external_module is None
    assert rec.explicit is False

    rec.spec.package.do_install(fake=True, explicit=True)
    rec = database.get_record('externaltool')
    assert rec.spec.external_path == '/path/to/external_tool'
    assert rec.spec.external_module is None
    assert rec.explicit is True


@pytest.mark.regression('8036')
def test_regression_issue_8036(mutable_database, usr_folder_exists):
    # The test ensures that the external package prefix is treated as
    # existing. Even when the package prefix exists, the package should
    # not be considered installed until it is added to the database with
    # do_install.
    s = spack.spec.Spec('externaltool@0.9')
    s.concretize()
    assert not s.package.installed

    # Now install the external package and check again the `installed` property
    s.package.do_install(fake=True)
    assert s.package.installed
