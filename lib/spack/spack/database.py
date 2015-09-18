##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Spack's installation tracking database.

The database serves two purposes:

  1. It implements a cache on top of a potentially very large Spack
     directory hierarchy, speeding up many operations that would
     otherwise require filesystem access.

  2. It will allow us to track external installations as well as lost
     packages and their dependencies.

Prior ot the implementation of this store, a direcotry layout served
as the authoritative database of packages in Spack.  This module
provides a cache and a sanity checking mechanism for what is in the
filesystem.

"""
import os
import time
import socket

from external import yaml
from external.yaml.error import MarkedYAMLError, YAMLError

import llnl.util.tty as tty
from llnl.util.filesystem import *
from llnl.util.lock import Lock

import spack.spec
from spack.version import Version
from spack.spec import Spec
from spack.error import SpackError

# DB goes in this directory underneath the root
_db_dirname = '.spack-db'

# DB version.  This is stuck in the DB file to track changes in format.
_db_version = Version('0.9')

# Default timeout for spack database locks is 5 min.
_db_lock_timeout = 300

def _autospec(function):
    """Decorator that automatically converts the argument of a single-arg
       function to a Spec."""
    def converter(self, spec_like, *args, **kwargs):
        if not isinstance(spec_like, spack.spec.Spec):
            spec_like = spack.spec.Spec(spec_like)
        return function(self, spec_like, *args, **kwargs)
    return converter


class InstallRecord(object):
    """A record represents one installation in the DB.

    The record keeps track of the spec for the installation, its
    install path, AND whether or not it is installed.  We need the
    installed flag in case a user either:

        a) blew away a directory, or
        b) used spack uninstall -f to get rid of it

    If, in either case, the package was removed but others still
    depend on it, we still need to track its spec, so we don't
    actually remove from the database until a spec has no installed
    dependents left.

    """
    def __init__(self, spec, path, installed):
        self.spec = spec
        self.path = path
        self.installed = installed
        self.ref_count = 0

    def to_dict(self):
        return { 'spec'      : self.spec.to_node_dict(),
                 'path'      : self.path,
                 'installed' : self.installed,
                 'ref_count' : self.ref_count }

    @classmethod
    def from_dict(cls, d):
        # TODO: check the dict more rigorously.
        return InstallRecord(d['spec'], d['path'], d['installed'], d['ref_count'])


class Database(object):
    def __init__(self, root):
        """Create an empty Database.

        Location defaults to root/_index.yaml
        The individual data are dicts containing
        spec: the top level spec of a package
        path: the path to the install of that package
        dep_hash: a hash of the dependence DAG for that package
        """
        self._root = root

        # Set up layout of database files.
        self._db_dir     = join_path(self._root, _db_dirname)
        self._index_path = join_path(self._db_dir, 'index.yaml')
        self._lock_path  = join_path(self._db_dir, 'lock')

        # Create needed directories and files
        if not os.path.exists(self._db_dir):
            mkdirp(self._db_dir)

        if not os.path.exists(self._lock_path):
            touch(self._lock_path)

        # initialize rest of state.
        self.lock = Lock(self._lock_path)
        self._data = {}
        self._last_write_time = 0


    def write_lock(self, timeout=_db_lock_timeout):
        """Get a write lock context for use in a `with` block."""
        return self.lock.write_lock(timeout)


    def read_lock(self, timeout=_db_lock_timeout):
        """Get a read lock context for use in a `with` block."""
        return self.lock.read_lock(timeout)


    def _write_to_yaml(self, stream):
        """Write out the databsae to a YAML file."""
        # map from per-spec hash code to installation record.
        installs = dict((k, v.to_dict()) for k, v in self._data.items())

        # databaes includes installation list and version.

        # NOTE: this DB version does not handle multiple installs of
        # the same spec well.  If there are 2 identical specs with
        # different paths, it can't differentiate.
        # TODO: fix this before we support multiple install locations.
        database = {
            'database' : {
                'installs' : installs,
                'version' : str(_db_version)
            }
        }

        try:
            return yaml.dump(database, stream=stream, default_flow_style=False)
        except YAMLError as e:
            raise SpackYAMLError("error writing YAML database:", str(e))


    def _read_spec_from_yaml(self, hash_key, installs, parent_key=None):
        """Recursively construct a spec from a hash in a YAML database."""
        if hash_key not in installs:
            parent = read_spec(installs[parent_key]['path'])

        spec_dict = installs[hash_key]['spec']

        # Build spec from dict first.
        spec = Spec.from_node_dict(spec_dict)

        # Add dependencies from other records in the install DB to
        # form a full spec.
        for dep_hash in spec_dict[spec.name]['dependencies'].values():
            child = self._read_spec_from_yaml(dep_hash, installs, hash_key)
            spec._add_dependency(child)

        return spec


    def _read_from_yaml(self, stream):
        """
        Fill database from YAML, do not maintain old data
        Translate the spec portions from node-dict form to spec form
        """
        try:
            if isinstance(stream, basestring):
                with open(stream, 'r') as f:
                    yfile = yaml.load(f)
            else:
                yfile = yaml.load(stream)

        except MarkedYAMLError as e:
            raise SpackYAMLError("error parsing YAML database:", str(e))

        if yfile is None:
            return

        def check(cond, msg):
            if not cond: raise CorruptDatabaseError(self._index_path, msg)

        check('database' in yfile, "No 'database' attribute in YAML.")

        # High-level file checks
        db = yfile['database']
        check('installs' in db, "No 'installs' in YAML DB.")
        check('version'  in db, "No 'version' in YAML DB.")

        # TODO: better version checking semantics.
        version = Version(db['version'])
        if version != _db_version:
            raise InvalidDatabaseVersionError(_db_version, version)

        # Iterate through database and check each record.
        installs = db['installs']
        data = {}
        for hash_key, rec in installs.items():
            try:
                # This constructs a spec DAG from the list of all installs
                spec = self._read_spec_from_yaml(hash_key, installs)

                # Validate the spec by ensuring the stored and actual
                # hashes are the same.
                spec_hash = spec.dag_hash()
                if not spec_hash == hash_key:
                    tty.warn("Hash mismatch in database: %s -> spec with hash %s"
                             % (hash_key, spec_hash))
                    continue    # TODO: is skipping the right thing to do?

                # Insert the brand new spec in the database.  Each
                # spec has its own copies of its dependency specs.
                # TODO: would a more immmutable spec implementation simplify this?
                data[hash_key] = InstallRecord(spec, rec['path'], rec['installed'])

            except Exception as e:
                tty.warn("Invalid database reecord:",
                         "file:  %s" % self._index_path,
                         "hash:  %s" % hash_key,
                         "cause: %s" % str(e))
                raise

        self._data = data


    def reindex(self, directory_layout):
        """Build database index from scratch based from a directory layout."""
        with self.write_lock():
            data = {}

            # Ask the directory layout to traverse the filesystem.
            for spec in directory_layout.all_specs():
                # Create a spec for each known package and add it.
                path = directory_layout.path_for_spec(spec)
                hash_key = spec.dag_hash()
                data[hash_key] = InstallRecord(spec, path, True)

                # Recursively examine dependencies and add them, even
                # if they are NOT installed.  This ensures we know
                # about missing dependencies.
                for dep in spec.traverse(root=False):
                    dep_hash = dep.dag_hash()
                    if dep_hash not in data:
                        path = directory_layout.path_for_spec(dep)
                        installed = os.path.isdir(path)
                        data[dep_hash] = InstallRecord(dep.copy(), path, installed)
                    data[dep_hash].ref_count += 1

            # Assuming everything went ok, replace this object's data.
            self._data = data

            # write out, blowing away the old version if necessary
            self.write()


    def read(self):
        """
        Re-read Database from the data in the set location
        If the cache is fresh, return immediately.
        """
        if not self.is_dirty():
            return

        if os.path.isfile(self._index_path):
            # Read from YAML file if a database exists
            self._read_from_yaml(self._index_path)
        else:
            # The file doesn't exist, try to traverse the directory.
            self.reindex(spack.install_layout)


    def write(self):
        """
        Write the database to the standard location
        Everywhere that the database is written it is read
        within the same lock, so there is no need to refresh
        the database within write()
        """
        temp_name = '%s.%s.temp' % (socket.getfqdn(), os.getpid())
        temp_file = join_path(self._db_dir, temp_name)

        # Write a temporary database file them move it into place
        try:
            with open(temp_file, 'w') as f:
                self._last_write_time = int(time.time())
                self._write_to_yaml(f)
            os.rename(temp_file, self._index_path)

        except:
            # Clean up temp file if something goes wrong.
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise


    def is_dirty(self):
        """
        Returns true iff the database file does not exist
        or was most recently written to by another spack instance.
        """
        return (not os.path.isfile(self._index_path) or
                (os.path.getmtime(self._index_path) > self._last_write_time))


    @_autospec
    def add(self, spec, path):
        """Read the database from the set location

        Add the specified entry as a dict, then write the database
        back to memory. This assumes that ALL dependencies are already in
        the database.  Should not be called otherwise.

        """
        # Should always already be locked
        with self.write_lock():
            self.read()
            self._data[spec.dag_hash()] = InstallRecord(spec, path, True)

            # sanity check the dependencies in case something went
            # wrong during install()
            # TODO: ensure no races during distributed install.
            for dep in spec.traverse(root=False):
                assert dep.dag_hash() in self._data

            self.write()


    @_autospec
    def remove(self, spec):
        """Removes a spec from the database.  To be called on uninstall.

        Reads the database, then:

          1. Marks the spec as not installed.
          2. Removes the spec if it has no more dependents.
          3. If removed, recursively updates dependencies' ref counts
             and remvoes them if they are no longer needed.

        """
        # Should always already be locked
        with self.write_lock():
            self.read()
            hash_key = spec.dag_hash()
            if hash_key in self._data:
                del self._data[hash_key]
            self.write()


    @_autospec
    def installed_extensions_for(self, extendee_spec):
        """
        Return the specs of all packages that extend
        the given spec
        """
        for s in self.query():
            try:
                if s.package.extends(extendee_spec):
                    yield s.package
            except UnknownPackageError as e:
                continue
            # skips unknown packages
            # TODO: conditional way to do this instead of catching exceptions


    def query(self, query_spec=any, known=any, installed=True):
        """Run a query on the database.

        ``query_spec``
            Queries iterate through specs in the database and return
            those that satisfy the supplied ``query_spec``.  If
            query_spec is `any`, This will match all specs in the
            database.  If it is a spec, we'll evaluate
            ``spec.satisfies(query_spec)``.

        The query can be constrained by two additional attributes:

        ``known``
            Possible values: True, False, any

            Specs that are "known" are those for which Spack can
            locate a ``package.py`` file -- i.e., Spack "knows" how to
            install them.  Specs that are unknown may represent
            packages that existed in a previous version of Spack, but
            have since either changed their name or been removed.

        ``installed``
            Possible values: True, False, any

            Specs for which a prefix exists are "installed". A spec
            that is NOT installed will be in the database if some
            other spec depends on it but its installation has gone
            away since Spack installed it.

        TODO: Specs are a lot like queries.  Should there be a
              wildcard spec object, and should specs have attributes
              like installed and known that can be queried?  Or are
              these really special cases that only belong here?

        """
        with self.read_lock():
            self.read()

        results = []
        for key, rec in self._data.items():
            if installed is not any and rec.installed != installed:
                continue
            if known is not any and spack.db.exists(rec.spec.name) != known:
                continue
            if query_spec is any or rec.spec.satisfies(query_spec):
                results.append(rec.spec)

        return sorted(results)


    def missing(self, spec):
        key =  spec.dag_hash()
        return key in self._data and not self._data[key].installed


class CorruptDatabaseError(SpackError):
    def __init__(self, path, msg=''):
        super(CorruptDatabaseError, self).__init__(
            "Spack database is corrupt: %s.  %s" %(path, msg))


class InvalidDatabaseVersionError(SpackError):
    def __init__(self, expected, found):
        super(InvalidDatabaseVersionError, self).__init__(
            "Expected database version %s but found version %s"
            % (expected, found))
