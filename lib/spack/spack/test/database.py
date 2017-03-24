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
"""
These tests check the database is functioning properly,
both in memory and in its file
"""
import multiprocessing
import os.path

import pytest
import spack
import spack.store
from llnl.util.tty.colify import colify


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


def _check_db_sanity(install_db):
    """Utiilty function to check db against install layout."""
    expected = sorted(spack.store.layout.all_specs())
    actual = sorted(install_db.query())

    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        assert e == a

    _check_merkleiness()


def _mock_remove(spec):
    specs = spack.store.db.query(spec)
    assert len(specs) == 1
    spec = specs[0]
    spec.package.do_uninstall(spec)


def test_default_queries(database):
    install_db = database.mock.db
    rec = install_db.get_record('zmpi')

    spec = rec.spec
    libraries = spec['zmpi'].libs
    assert len(libraries) == 1

    cppflags_expected = '-I' + spec.prefix.include
    assert spec['zmpi'].cppflags == cppflags_expected


def test_005_db_exists(database):
    """Make sure db cache file exists after creating."""
    install_path = database.mock.path
    index_file = install_path.join('.spack-db', 'index.json')
    lock_file = install_path.join('.spack-db', 'lock')
    assert os.path.exists(str(index_file))
    assert os.path.exists(str(lock_file))


def test_010_all_install_sanity(database):
    """Ensure that the install layout reflects what we think it does."""
    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 13

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
    assert len([s for s in all_specs if s.satisfies('mpileaks ^mpich')]) == 1
    assert len([s for s in all_specs if s.satisfies('mpileaks ^mpich2')]) == 1
    assert len([s for s in all_specs if s.satisfies('mpileaks ^zmpi')]) == 1


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
    install_db = database.mock.db
    _check_db_sanity(install_db)


def test_025_reindex(database):
    """Make sure reindex works and ref counts are valid."""
    install_db = database.mock.db
    spack.store.db.reindex(spack.store.layout)
    _check_db_sanity(install_db)


def test_030_db_sanity_from_another_process(database, refresh_db_on_exit):
    install_db = database.mock.db

    def read_and_modify():
        _check_db_sanity(install_db)  # check that other process can read DB
        with install_db.write_transaction():
            _mock_remove('mpileaks ^zmpi')

    p = multiprocessing.Process(target=read_and_modify, args=())
    p.start()
    p.join()

    # ensure child process change is visible in parent process
    with install_db.read_transaction():
        assert len(install_db.query('mpileaks ^zmpi')) == 0


def test_040_ref_counts(database):
    """Ensure that we got ref counts right when we read the DB."""
    install_db = database.mock.db
    install_db._check_ref_counts()


def test_050_basic_query(database):
    """Ensure querying database is consistent with what is installed."""
    install_db = database.mock.db
    # query everything
    assert len(spack.store.db.query()) == 13

    # query specs with multiple configurations
    mpileaks_specs = install_db.query('mpileaks')
    callpath_specs = install_db.query('callpath')
    mpi_specs = install_db.query('mpi')

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # query specs with single configurations
    dyninst_specs = install_db.query('dyninst')
    libdwarf_specs = install_db.query('libdwarf')
    libelf_specs = install_db.query('libelf')

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(install_db.query('mpileaks ^mpich')) == 1
    assert len(install_db.query('mpileaks ^mpich2')) == 1
    assert len(install_db.query('mpileaks ^zmpi')) == 1


def _check_remove_and_add_package(install_db, spec):
    """Remove a spec from the DB, then add it and make sure everything's
    still ok once it is added.  This checks that it was
    removed, that it's back when added again, and that ref
    counts are consistent.
    """
    original = install_db.query()
    install_db._check_ref_counts()

    # Remove spec
    concrete_spec = install_db.remove(spec)
    install_db._check_ref_counts()
    remaining = install_db.query()

    # ensure spec we removed is gone
    assert len(original) - 1 == len(remaining)
    assert all(s in original for s in remaining)
    assert concrete_spec not in remaining

    # add it back and make sure everything is ok.
    install_db.add(concrete_spec, spack.store.layout)
    installed = install_db.query()
    assert concrete_spec in installed
    assert installed == original

    # sanity check against direcory layout and check ref counts.
    _check_db_sanity(install_db)
    install_db._check_ref_counts()


def test_060_remove_and_add_root_package(database):
    install_db = database.mock.db
    _check_remove_and_add_package(install_db, 'mpileaks ^mpich')


def test_070_remove_and_add_dependency_package(database):
    install_db = database.mock.db
    _check_remove_and_add_package(install_db, 'dyninst')


def test_080_root_ref_counts(database):
    install_db = database.mock.db
    rec = install_db.get_record('mpileaks ^mpich')

    # Remove a top-level spec from the DB
    install_db.remove('mpileaks ^mpich')

    # record no longer in DB
    assert install_db.query('mpileaks ^mpich', installed=any) == []

    # record's deps have updated ref_counts
    assert install_db.get_record('callpath ^mpich').ref_count == 0
    assert install_db.get_record('mpich').ref_count == 1

    # Put the spec back
    install_db.add(rec.spec, spack.store.layout)

    # record is present again
    assert len(install_db.query('mpileaks ^mpich', installed=any)) == 1

    # dependencies have ref counts updated
    assert install_db.get_record('callpath ^mpich').ref_count == 1
    assert install_db.get_record('mpich').ref_count == 2


def test_090_non_root_ref_counts(database):
    install_db = database.mock.db

    install_db.get_record('mpileaks ^mpich')
    install_db.get_record('callpath ^mpich')

    # "force remove" a non-root spec from the DB
    install_db.remove('callpath ^mpich')

    # record still in DB but marked uninstalled
    assert install_db.query('callpath ^mpich', installed=True) == []
    assert len(install_db.query('callpath ^mpich', installed=any)) == 1

    # record and its deps have same ref_counts
    assert install_db.get_record(
        'callpath ^mpich', installed=any
    ).ref_count == 1
    assert install_db.get_record('mpich').ref_count == 2

    # remove only dependent of uninstalled callpath record
    install_db.remove('mpileaks ^mpich')

    # record and parent are completely gone.
    assert install_db.query('mpileaks ^mpich', installed=any) == []
    assert install_db.query('callpath ^mpich', installed=any) == []

    # mpich ref count updated properly.
    mpich_rec = install_db.get_record('mpich')
    assert mpich_rec.ref_count == 0


def test_100_no_write_with_exception_on_remove(database):
    install_db = database.mock.db

    def fail_while_writing():
        with install_db.write_transaction():
            _mock_remove('mpileaks ^zmpi')
            raise Exception()

    with install_db.read_transaction():
        assert len(install_db.query('mpileaks ^zmpi', installed=any)) == 1

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure zmpi is still there.
    with install_db.read_transaction():
        assert len(install_db.query('mpileaks ^zmpi', installed=any)) == 1


def test_110_no_write_with_exception_on_install(database):
    install_db = database.mock.db

    def fail_while_writing():
        with install_db.write_transaction():
            _mock_install('cmake')
            raise Exception()

    with install_db.read_transaction():
        assert install_db.query('cmake', installed=any) == []

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure cmake was not written.
    with install_db.read_transaction():
        assert install_db.query('cmake', installed=any) == []
