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

import spack
import spack.store
from llnl.util.filesystem import join_path
from llnl.util.tty.colify import colify
from spack.test.mock_database import MockDatabase


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


class DatabaseTest(MockDatabase):

    def test_005_db_exists(self):
        """Make sure db cache file exists after creating."""
        index_file = join_path(self.install_path, '.spack-db', 'index.json')
        lock_file = join_path(self.install_path, '.spack-db', 'lock')

        self.assertTrue(os.path.exists(index_file))
        self.assertTrue(os.path.exists(lock_file))

    def test_010_all_install_sanity(self):
        """Ensure that the install layout reflects what we think it does."""
        all_specs = spack.store.layout.all_specs()
        self.assertEqual(len(all_specs), 13)

        # query specs with multiple configurations
        mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
        callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
        mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

        self.assertEqual(len(mpileaks_specs), 3)
        self.assertEqual(len(callpath_specs), 3)
        self.assertEqual(len(mpi_specs),      3)

        # query specs with single configurations
        dyninst_specs = [s for s in all_specs if s.satisfies('dyninst')]
        libdwarf_specs = [s for s in all_specs if s.satisfies('libdwarf')]
        libelf_specs = [s for s in all_specs if s.satisfies('libelf')]

        self.assertEqual(len(dyninst_specs),  1)
        self.assertEqual(len(libdwarf_specs), 1)
        self.assertEqual(len(libelf_specs),   1)

        # Query by dependency
        self.assertEqual(
            len([s for s in all_specs if s.satisfies('mpileaks ^mpich')]), 1)
        self.assertEqual(
            len([s for s in all_specs if s.satisfies('mpileaks ^mpich2')]), 1)
        self.assertEqual(
            len([s for s in all_specs if s.satisfies('mpileaks ^zmpi')]), 1)

    def test_015_write_and_read(self):
        # write and read DB
        with spack.store.db.write_transaction():
            specs = spack.store.db.query()
            recs = [spack.store.db.get_record(s) for s in specs]

        for spec, rec in zip(specs, recs):
            new_rec = spack.store.db.get_record(spec)
            self.assertEqual(new_rec.ref_count, rec.ref_count)
            self.assertEqual(new_rec.spec,      rec.spec)
            self.assertEqual(new_rec.path,      rec.path)
            self.assertEqual(new_rec.installed, rec.installed)

    def _check_merkleiness(self):
        """Ensure the spack database is a valid merkle graph."""
        all_specs = spack.store.db.query(installed=any)

        seen = {}
        for spec in all_specs:
            for dep in spec.dependencies():
                hash_key = dep.dag_hash()
                if hash_key not in seen:
                    seen[hash_key] = id(dep)
                else:
                    self.assertEqual(seen[hash_key], id(dep))

    def _check_db_sanity(self):
        """Utiilty function to check db against install layout."""
        expected = sorted(spack.store.layout.all_specs())
        actual = sorted(self.install_db.query())

        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

        self._check_merkleiness()

    def test_020_db_sanity(self):
        """Make sure query() returns what's actually in the db."""
        self._check_db_sanity()

    def test_025_reindex(self):
        """Make sure reindex works and ref counts are valid."""
        spack.store.db.reindex(spack.store.layout)
        self._check_db_sanity()

    def test_030_db_sanity_from_another_process(self):
        def read_and_modify():
            self._check_db_sanity()  # check that other process can read DB
            with self.install_db.write_transaction():
                self._mock_remove('mpileaks ^zmpi')

        p = multiprocessing.Process(target=read_and_modify, args=())
        p.start()
        p.join()

        # ensure child process change is visible in parent process
        with self.install_db.read_transaction():
            self.assertEqual(len(self.install_db.query('mpileaks ^zmpi')), 0)

    def test_040_ref_counts(self):
        """Ensure that we got ref counts right when we read the DB."""
        self.install_db._check_ref_counts()

    def test_050_basic_query(self):
        """Ensure querying database is consistent with what is installed."""
        # query everything
        self.assertEqual(len(spack.store.db.query()), 13)

        # query specs with multiple configurations
        mpileaks_specs = self.install_db.query('mpileaks')
        callpath_specs = self.install_db.query('callpath')
        mpi_specs = self.install_db.query('mpi')

        self.assertEqual(len(mpileaks_specs), 3)
        self.assertEqual(len(callpath_specs), 3)
        self.assertEqual(len(mpi_specs),      3)

        # query specs with single configurations
        dyninst_specs = self.install_db.query('dyninst')
        libdwarf_specs = self.install_db.query('libdwarf')
        libelf_specs = self.install_db.query('libelf')

        self.assertEqual(len(dyninst_specs),  1)
        self.assertEqual(len(libdwarf_specs), 1)
        self.assertEqual(len(libelf_specs),   1)

        # Query by dependency
        self.assertEqual(len(self.install_db.query('mpileaks ^mpich')),  1)
        self.assertEqual(len(self.install_db.query('mpileaks ^mpich2')), 1)
        self.assertEqual(len(self.install_db.query('mpileaks ^zmpi')),   1)

    def _check_remove_and_add_package(self, spec):
        """Remove a spec from the DB, then add it and make sure everything's
           still ok once it is added.  This checks that it was
           removed, that it's back when added again, and that ref
           counts are consistent.
        """
        original = self.install_db.query()
        self.install_db._check_ref_counts()

        # Remove spec
        concrete_spec = self.install_db.remove(spec)
        self.install_db._check_ref_counts()
        remaining = self.install_db.query()

        # ensure spec we removed is gone
        self.assertEqual(len(original) - 1, len(remaining))
        self.assertTrue(all(s in original for s in remaining))
        self.assertTrue(concrete_spec not in remaining)

        # add it back and make sure everything is ok.
        self.install_db.add(concrete_spec, spack.store.layout)
        installed = self.install_db.query()
        self.assertTrue(concrete_spec in installed)
        self.assertEqual(installed, original)

        # sanity check against direcory layout and check ref counts.
        self._check_db_sanity()
        self.install_db._check_ref_counts()

    def test_060_remove_and_add_root_package(self):
        self._check_remove_and_add_package('mpileaks ^mpich')

    def test_070_remove_and_add_dependency_package(self):
        self._check_remove_and_add_package('dyninst')

    def test_080_root_ref_counts(self):
        rec = self.install_db.get_record('mpileaks ^mpich')

        # Remove a top-level spec from the DB
        self.install_db.remove('mpileaks ^mpich')

        # record no longer in DB
        self.assertEqual(
            self.install_db.query('mpileaks ^mpich', installed=any), [])

        # record's deps have updated ref_counts
        self.assertEqual(
            self.install_db.get_record('callpath ^mpich').ref_count, 0)
        self.assertEqual(self.install_db.get_record('mpich').ref_count, 1)

        # Put the spec back
        self.install_db.add(rec.spec, spack.store.layout)

        # record is present again
        self.assertEqual(
            len(self.install_db.query('mpileaks ^mpich', installed=any)), 1)

        # dependencies have ref counts updated
        self.assertEqual(
            self.install_db.get_record('callpath ^mpich').ref_count, 1)
        self.assertEqual(self.install_db.get_record('mpich').ref_count, 2)

    def test_090_non_root_ref_counts(self):
        self.install_db.get_record('mpileaks ^mpich')
        self.install_db.get_record('callpath ^mpich')

        # "force remove" a non-root spec from the DB
        self.install_db.remove('callpath ^mpich')

        # record still in DB but marked uninstalled
        self.assertEqual(
            self.install_db.query('callpath ^mpich', installed=True), [])
        self.assertEqual(
            len(self.install_db.query('callpath ^mpich', installed=any)), 1)

        # record and its deps have same ref_counts
        self.assertEqual(self.install_db.get_record(
            'callpath ^mpich', installed=any).ref_count, 1)
        self.assertEqual(self.install_db.get_record('mpich').ref_count, 2)

        # remove only dependent of uninstalled callpath record
        self.install_db.remove('mpileaks ^mpich')

        # record and parent are completely gone.
        self.assertEqual(
            self.install_db.query('mpileaks ^mpich', installed=any), [])
        self.assertEqual(
            self.install_db.query('callpath ^mpich', installed=any), [])

        # mpich ref count updated properly.
        mpich_rec = self.install_db.get_record('mpich')
        self.assertEqual(mpich_rec.ref_count, 0)

    def test_100_no_write_with_exception_on_remove(self):
        def fail_while_writing():
            with self.install_db.write_transaction():
                self._mock_remove('mpileaks ^zmpi')
                raise Exception()

        with self.install_db.read_transaction():
            self.assertEqual(
                len(self.install_db.query('mpileaks ^zmpi', installed=any)),
                1)

        self.assertRaises(Exception, fail_while_writing)

        # reload DB and make sure zmpi is still there.
        with self.install_db.read_transaction():
            self.assertEqual(
                len(self.install_db.query('mpileaks ^zmpi', installed=any)),
                1)

    def test_110_no_write_with_exception_on_install(self):
        def fail_while_writing():
            with self.install_db.write_transaction():
                self._mock_install('cmake')
                raise Exception()

        with self.install_db.read_transaction():
            self.assertEqual(
                self.install_db.query('cmake', installed=any), [])

        self.assertRaises(Exception, fail_while_writing)

        # reload DB and make sure cmake was not written.
        with self.install_db.read_transaction():
            self.assertEqual(
                self.install_db.query('cmake', installed=any), [])
